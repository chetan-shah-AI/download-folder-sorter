import os
from file_classfier import get_destination_folder

def test_dst_folder():
    
    # Test case 1: File with .jpg extension should go to Pictures folder
    file_name = "photo.jpg"
    expected_folder = "Pictures"
    print(f"Testing with file: {file_name}")
    assert get_destination_folder(file_name) == expected_folder

    # Test case 2: File with .pdf extension should go to PDFs folder
    file_name = "document.pdf"
    expected_folder = "PDFs"
    print(f"Testing with file: {file_name}")
    assert get_destination_folder(file_name) == expected_folder
