from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

# Khởi tạo trình duyệt
s = Service('D:\KHDL\DuDoanGiaKhachSan\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Mở trang web booking.com
driver.get("https://www.booking.com/index.vi.html")

time.sleep(5)

# tạo mảng serch_input


# bỏ qua phần đăng nhập 

close_pane = driver.find_element(By.CSS_SELECTOR,"[aria-label='Bỏ qua phần đăng nhập.']")
close_pane.click()

time.sleep(0.5)

# Tìm thẻ input để nhập địa điểm
search_input = driver.find_element(By.NAME,"ss")
# Nhập địa điểm "Paris" vào ô tìm kiếm
hotel_country = "Indonesia"
hotel_place = "Bali"
search_input.send_keys(hotel_place)
time.sleep(0.5)


# date_starts = driver.find_elements(By.CSS_SELECTOR,"[data-testid='property-card']")
# print(len(date_starts))

# Tìm thẻ input để nhập ngày check-in và check-out
# nhập bắt đầu kết thúc
date_start = driver.find_element(By.CSS_SELECTOR,"[data-testid='date-display-field-start']")
date_start.click()
time.sleep(0.5)

checkin_input = driver.find_element(By.CSS_SELECTOR,"[data-date='2023-05-30']")
checkin_input.click()
time.sleep(0.5)

# date_end = driver.find_element(By.CSS_SELECTOR,"[data-testid='date-display-field-end']")
# date_end.click()

checkin_output = driver.find_element(By.CSS_SELECTOR,"[data-date='2023-05-31']")
checkin_output.click()
time.sleep(0.5)

# Tìm thẻ button để tìm kiếm
search_button = driver.find_element(By.CSS_SELECTOR,'.fc63351294.a822bdf511.d4b6b7a9e7.cfb238afa1.c938084447.f4605622ad.aa11d0d5cd')
# Kích hoạt button để tìm kiếm
search_button.click()
time.sleep(0.5)

list_hotel = []
for i in range(1,2,1): 
    time.sleep(5)
    # lấy các div chứa thông tin khách sạn
    hotel_infos = driver.find_elements(By.CSS_SELECTOR,"[data-testid='property-card']")
    print(len(hotel_infos))
    for hotel_info in hotel_infos:
        hotel_name = hotel_info.find_element(By.CSS_SELECTOR,"[data-testid='title']").text
        hotel_price = hotel_info.find_element(By.CSS_SELECTOR,"[data-testid='price-and-discounted-price']").text
        hotel_tax = hotel_info.find_element(By.CSS_SELECTOR,"[data-testid='taxes-and-charges']").text
        hotel_stars = len(hotel_info.find_element(By.CSS_SELECTOR,"[data-testid='rating-stars']").find_elements(By.TAG_NAME,"span")) if len(hotel_info.find_elements(By.CSS_SELECTOR,"[data-testid='rating-stars']"))!=0 else None
        hotel_distance = hotel_info.find_element(By.CSS_SELECTOR,"[data-testid='distance']").text if len(hotel_info.find_elements(By.CSS_SELECTOR,"[data-testid='distance']"))!=0 else None 
        hotel_number_review = hotel_info.find_element(By.CSS_SELECTOR,".d8eab2cf7f.c90c0a70d3.db63693c62").text if len(hotel_info.find_elements(By.CSS_SELECTOR,".d8eab2cf7f.c90c0a70d3.db63693c62"))!=0 else None
        hotel_sustainable_level = hotel_info.find_element(By.CSS_SELECTOR,".d8eab2cf7f.be09c104ad").text if len(hotel_info.find_elements(By.CSS_SELECTOR,".d8eab2cf7f.be09c104ad"))!=0 else None
        hotel_discount = "Ưu Đãi Mùa Du Lịch" in hotel_info.text
        hotel_point = hotel_info.find_element(By.CSS_SELECTOR,".b5cd09854e.d10a6220b4").text if len(hotel_info.find_elements(By.CSS_SELECTOR,".b5cd09854e.d10a6220b4"))!=0 else None
        hotel_free_breakfast = "Bao bữa sáng" in hotel_info.text
        hotel_is_prepayment = "Không cần thanh toán trước" in hotel_info.text
        hotel_is_notable_place = "Nổi bật" in hotel_info.text
        hotel_is_free_cancel = ("Miễn phí hủy" in hotel_info.text) or ("Miễn Phí hủy phòng" in hotel_info.text)
        hotel_is_sold_out = "phòng với giá này trên trang của chúng tôi" in hotel_info.text
        
        print("hotel_info: ",hotel_info.text)
        # print("hotel_name: ",hotel_name, end=" | ")
        # print("hotel_price: ",hotel_price, end=" | ")
        # print("hotel_tax: ",hotel_tax, end=" | ")
        # print("hotel_stars: ",hotel_stars, end=" | ")
        # print("hotel_distance: ",hotel_distance, end=" | ")
        # print("hotel_number_review: ",hotel_number_review, end=" | ")
        # print("hotel_sustainable_level: ",hotel_sustainable_level, end=" | ")
        # print("hotel_discount: ",hotel_discount, end=" | ")
        # print("hotel_point: ",hotel_point)
        
        list_hotel.append([hotel_country,hotel_place,hotel_name,hotel_price,hotel_tax,hotel_stars,
                           hotel_distance,hotel_number_review,hotel_sustainable_level,
                           hotel_discount,hotel_free_breakfast,hotel_is_prepayment,
                           hotel_is_notable_place,hotel_is_free_cancel,hotel_is_sold_out,hotel_point])
    try:
        page_index_button = driver.find_element(By.CSS_SELECTOR,f"[aria-label=' {i+1}']")
        page_index_button.click()
    except:
        break
    
# Đóng trình duyệt
driver.quit()

# print(list_hotel)
# Đọc file CSV vào DataFrame
# df = pd.read_csv('hotel_foreign.csv')
df_hotel = pd.DataFrame(list_hotel, columns=['Country','Place', 'Name', 'Price', 'Tax', 
                                             'Stars', 'Distance', 'Number_of_review', 
                                             'Sustainable_level', 'Discount',
                                             'Free_Breakfast', 'is_Prepayment',
                                             'is_NotablePlace', 'is_Free_Cancel',
                                             'is_Sold_Out', 'Point'])
# df_new = pd.concat([df, df_hotel], ignore_index=True)0
df_hotel.to_csv('Hotel_data.csv', index=False, encoding='utf-8-sig')