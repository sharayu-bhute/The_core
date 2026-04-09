def classify_image(image_path):
    # Dummy logic (replace later with real ML)
    if "road" in image_path:
        return "pothole"
    elif "garbage" in image_path:
        return "garbage"
    else:
        return "water"