def check_valid_page_count(page_count):
    if not isinstance(page_count, int) or page_count <= 0:
        return False
    return True

def is_sufficient_ink(ink, pages_to_print):
    # Calculate the number of pages the current ink level can print
    ink_level = ink["level"]
    max_print_pages = ink["max_print_pages"]

    pages_that_can_be_printed = (int)((ink_level / 100) * max_print_pages)
    
    # Check if there is enough ink to print the requested pages
    if pages_that_can_be_printed >= pages_to_print:
        return True
    else:
        return False
    
def calculate_ink_usage(ink, pages_to_print):
    ink_level = ink["level"]
    max_print_pages = ink["max_print_pages"]

    pages_that_can_be_printed = (int)((ink_level / 100) * max_print_pages)

    # Tính toán lượng mực sẽ bị tiêu thụ khi in pages_to_print trang
    if pages_to_print <= pages_that_can_be_printed:
        # Lượng mực tiêu thụ theo tỷ lệ trang in
        ink_used_percentage = (pages_to_print / max_print_pages) * 100
    else:
        ink_used_percentage = ink_level  # Nếu không đủ mực, sẽ dùng hết

    return ink_used_percentage  # Trả về lượng mực sẽ bị tiêu thụ