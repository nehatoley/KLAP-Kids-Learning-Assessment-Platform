from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
import os
import time

model = YOLO("yolov8n.pt")

def camera_page(request):
    return render(request, "camera.html")

@csrf_exempt
def detect_api(request):
    if request.method == "POST":
        print(request.FILES)

        image = request.FILES.get("image")

        if not image:
            return JsonResponse({"error": "No image received"})

        media_path = os.path.join(settings.BASE_DIR, "media")
        os.makedirs(media_path, exist_ok=True)

        filename = f"frame_{int(time.time())}.jpg"
        path = os.path.join(media_path, filename)

        with open(path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        results = model(path)

        names = set()
        best_label = None
        best_conf = 0
        person_detected = False

        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    conf = float(box.conf)
                    label = model.names[int(box.cls)]

                    if label == "person":
                        person_detected = True

                    elif conf > best_conf:
                        best_conf = conf
                        best_label = label

        if best_label:
            return JsonResponse({"detected": [best_label]})
        elif person_detected:
            return JsonResponse({"detected": ["person"]})
        else:
            return JsonResponse({"detected": []})