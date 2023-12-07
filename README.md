# Parallel-Computing-App

HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

I. Những thư viện cần thiết:
1. Thư viện Python:
- colorsys
- cupy
- fastapi
- imageio
- imutils
- matplotlib.pyplot
- numba
- numpy
- opencv
- pydantic
- scipy
- sklearn.mixture
2. Thư viện React:
- axios
- react
- react-dom
- react-router-dom

II. Sử dụng ứng dụng:
1. Về ứng dụng:
- Ứng dụng có 2 features: FCM và FCM2
- FCM là chương trình phát hiện u não dùng thư viện có sẵn
- FCM 2 là chương trình phát hiện u não do nhóm tự thiết kế
- Ứng dụng sẽ phát hiện u não và tô màu khối u
![Alt text](image1.png)

2. Thiết lập:
- Trước tiên người dùng cần cài các thư viện cần thiết đã liệt kê ở trên
- Về input:
    + Chương trình sẽ nhận file ảnh y tế DICOM nên file cần có dạng ".dcm"
    + Hãy đưa ảnh MRI muốn xử lý vào folder "img" 
    + Nếu muốn dùng chương trình FCM, hãy đưa ảnh vào folder "MAIN_APP/FCM/img", còn FCM 2 thì đưa vào folder "MAIN_APP/FCM_Parallel/img"
    + Trong folder img của cả 2 chương trình đã có sẵn 4 file DICOM MRI chứa u não
- Về output:
    + Sau khi nhận ảnh và xử lý, chương trình sẽ lưu ảnh mới
    + Trước khi dùng, người dùng cần phải thiết lập folder output để chương trình lưu ảnh vào
    + Trong folder FCM sửa nội dung của file .env: OUTPUT_PATH = (Đường dẫn thư mục output mong muốn) để lưu kết quả cho chương trình FCM
    + Tương tự cho chương trình FCM 2, sửa file .env: OUTPUT_PATH2 = (Đường dẫn thư mục output mong muốn)
    + Người dùng có thể sử dụng 2 folder "MAIN_APP/FCM/output" và "MAIN_APP/FCM_Parallel/output" đã được tạo sẵn

3. Dùng ứng dụng:
- Bước 1: Khởi động ReactJS và FastAPI:
    + Mở terminal tại folder "MAIN_APP/main-app", nhập: npm start
    + Mở terminal tại folder "MAIN_APP/FCM", nhập: uvicorn app:app --port 8000
    + Mở terminal tại folder "MAIN_APP/FCM_Parallel", nhập: uvicorn app:app --port 8001
- Bước 2: Tương tác với giao diện: 
    + Thanh điều hướng ở trên cùng có 4 nút: Home, About us, FCM và FCM 2. 
    + Hướng dẫn này sử dụng chương trình FCM 2
    ![Alt text](image2.png)
    + Ấn nút "Choose file" để chọn file ảnh MRI muốn xử lý và lựa chọn file trong folder "MAIN_APP/FCM_Parallel/img"
    + Lựa chọn bên dưới: 1 là chạy song song, 2 là chạy tuần tự
    + Sau đó ấn nút "OK" và đợi vài giây để chương trình xử lý
    + Khi chương trình xử lý xong, in ra màn hình tiếp theo là đường dẫn đến ảnh mới, cùng nút "Kết quả"
    + Khi ấn nút "Kết quả", ảnh mới đã được xử lý đó sẽ được in ra màn hình
    ![Alt text](image3.png)
    + Để dùng chương trình FCM, chọn file trong folder "MAIN_APP/FCM/img", không cần bước chọn option, còn lại chạy giống như trên