# Define file type categories and their regex patterns
FILE_TYPE_CATEGORIES = {
    "Images": r"\.(jpg|jpeg|gif|bmp|tiff|svg)$",
    "Documents": r"\.(pdf|doc|docx|xls|xlsx|ppt|pptx|txt)$",
    "Videos": r"\.(mp4|avi|mov|mkv|flv|wmv|webm)$",
    "Audio": r"\.(mp3|wav|aac|flac|ogg|wma)$",
    "Archives": r"\.(zip|rar|7z|tar|gz)$",
    "Code": r"\.(java|cpp|js|html|css|sh|bat|rb|php|py)$",
    "Other": r"\.()$",
}