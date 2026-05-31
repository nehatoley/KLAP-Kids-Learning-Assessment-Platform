from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ultralytics import YOLO

from detection.models import LearningLog
from parents.models import Child

import os
import time


# =====================================
# LOAD MODELS
# =====================================

fruit_model = YOLO("fruit_model.pt")

animal_model = YOLO("animal_model.pt")

new_animal_model = YOLO("new_animal.pt")

vegetable_model = YOLO("vegetable.pt")


# =====================================
# CAMERA PAGE
# =====================================

def camera_page(request):

    category = request.GET.get("category")

    child_id = request.GET.get("child_id")

    # DEFAULT
    mode = "teacher"

    # AGAR CHILD ID HAI → PARENT
    if child_id:

        mode = "parent"

    return render(

        request,

        "camera.html",

        {
            "category": category,
            "child_id": child_id,
            "mode": mode
        }
    )


# =====================================
# DETECT API
# =====================================

@csrf_exempt
def detect_api(request):

    if request.method != "POST":

        return JsonResponse({
            "error": "Only POST method allowed"
        })

    try:

        # =====================================
        # GET IMAGE + CATEGORY + CHILD
        # =====================================

        image = request.FILES.get("image")

        category = request.POST.get("category")

        child_id = request.POST.get("child_id")

        print("CATEGORY:", category)
        print("CHILD ID:", child_id)

        if not image:

            return JsonResponse({
                "error": "No image received"
            })

        # =====================================
        # CREATE MEDIA FOLDER
        # =====================================

        media_path = os.path.join(
            settings.BASE_DIR,
            "media"
        )

        os.makedirs(media_path, exist_ok=True)

        # =====================================
        # SAVE IMAGE
        # =====================================

        filename = f"img_{int(time.time())}.jpg"

        image_path = os.path.join(
            media_path,
            filename
        )

        with open(image_path, "wb+") as f:

            for chunk in image.chunks():

                f.write(chunk)

        print("IMAGE SAVED:", image_path)

        # =====================================
        # MODEL RESULTS
        # =====================================

        model_results = []

        # =====================================
        # FRUIT MODEL
        # =====================================

        if category == "fruit":

            results = fruit_model(
                image_path,
                conf=0.05
            )

            model_results.append(
                (results, fruit_model)
            )

        # =====================================
        # ANIMAL MODEL
        # =====================================

        elif category == "animal":

            results1 = animal_model(
                image_path,
                conf=0.05
            )

            results2 = new_animal_model(
                image_path,
                conf=0.05
            )

            model_results.append(
                (results1, animal_model)
            )

            model_results.append(
                (results2, new_animal_model)
            )

        # =====================================
        # VEGETABLE MODEL
        # =====================================

        elif category == "vegetable":

            results = vegetable_model(
                image_path,
                conf=0.05
            )

            model_results.append(
                (results, vegetable_model)
            )

        # =====================================
        # INVALID CATEGORY
        # =====================================

        else:

            return JsonResponse({

                "detected": [],

                "message": "Invalid category"

            })

        # =====================================
        # FIND BEST DETECTION
        # =====================================

        best_label = None
        best_conf = 0

        for results, current_model in model_results:

            for r in results:

                if r.boxes is not None:

                    for box in r.boxes:

                        conf = float(box.conf)

                        label = current_model.names[
                            int(box.cls)
                        ]

                        print("LABEL:", label)
                        print("CONF:", conf)

                        # TAKE BEST RESULT

                        if conf > best_conf:

                            best_conf = conf
                            best_label = label

        # =====================================
        # SAVE LEARNING LOG
        # =====================================

        if best_label and child_id:

            try:

                child = Child.objects.get(
                    id=child_id
                )

                LearningLog.objects.create(

                    child=child,

                    object_name=best_label,

                    category=category,

                    confidence=round(best_conf, 2)

                )

                print("✅ Learning Saved")

            except Exception as e:

                print("❌ Learning Save Error:", e)

        # =====================================
        # FINAL RESPONSE
        # =====================================

        if best_label:

            return JsonResponse({

                "detected": [best_label],

                "confidence": round(best_conf, 2)

            })

        return JsonResponse({

            "detected": [],

            "message": "No object detected"

        })

    except Exception as e:

        print("ERROR:", str(e))

        return JsonResponse({

            "error": str(e)

        })