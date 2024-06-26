import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile

from backend.services.image_service import predict_and_plot

router = APIRouter(
    prefix="/api/detect",
    tags=["detect"],
    responses={404: {"description": "The requested url was not found"}},
)


@router.post("")
async def detect(
        image: UploadFile = File(...)
):
    # Base 64 decode the image
    if image and image.content_type != "image/jpeg":
        return {300: {"description": "Only jpeg images are supported"}}
    else:
        contents = await image.read()
        nparray = np.fromstring(contents, np.uint8)
        img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)

    # Run the model on the image
    predicted_label, image = predict_and_plot(img)

    # Return the result
    return {"prediction": predicted_label, "image": image}
