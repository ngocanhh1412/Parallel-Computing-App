import React, { useState, useEffect } from "react";
import { callAddAPI } from "./Api";
import { callAddAPI2 } from "./Api2";
import { BrowserRouter as Router, Route, Link, Switch , NavLink, Routes } from 'react-router-dom';
import Nav from './Components/Nav';
import './App.css';
import './Components/AboutUs.css';
import ImageComponent from "./ImageComponent";
import ImageComponent2 from "./ImageComponent2";
// import axios from "axios";

function Home() {
  return (
    <div className="center">
      <h1>Đây là chương trình phát hiện khối u não</h1>
      <p>Hãy chọn file ảnh DICOM MRI cần xử lý</p>
      <p>Ảnh sẽ được xử lý, sau đó ảnh mới sẽ được lưu vào file /output</p>
    </div>
  );
}

function AboutUs() {
  return (
    <div>
      <h1>Nhóm 2:</h1>
      {/* <p>Dương Ngọc Thái</p>
      <p>Mai Bá Đức</p>
      <p>Hoàng Xuân Quý</p>
      <p>Nguyễn Ngọc Anh</p> */}

      <table className="table">
        <tr className="th">
            <th>Tên thành viên</th>
            <th>Nhiệm vụ</th>
        </tr>
        <tr>
            <td>Dương Ngọc Thái</td>
            <td>Thiết kế thuật toán FCM tuần tự</td>
        </tr>
        <tr>
            <td>Hoàng Xuân Quý</td>
            <td>Xử lý thuật toán FCM song song</td>
        </tr>
        <tr>
            <td>Mai Bá Đức</td>
            <td>Xử lý dữ liệu và tìm u não</td>
        </tr>
        <tr>
            <td>Nguyễn Ngọc Anh</td>
            <td>Thiết kế ứng dụng</td>
        </tr>
      </table>
    </div>
  );
}

function FCM() {
  const [result, setResult] = useState("");
  const [showButton, setShowButton] = useState(false);

  const [showImageComponent, setShowImageComponent] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleAddClick = async () => {
    try {
      // const result = await callAddAPI(inputString);
      const result = await callAddAPI(selectedFile.name);
      setResult(result);
      setShowButton(true);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleButtonClick = () => {
    setResult(result);
    setShowImageComponent(true);
  };

  return (
    <div>
      <h1>FCM: USING LIBRARIES</h1>
      {/* <input type="text" value={inputString} onChange={handleInputChange} /> */}
      
      <input className="custom-file-input"
        type="file"
        accept=".dcm"
        onChange={handleFileChange}
      />
      {selectedFile && <p>Tên tệp đã chọn: {selectedFile.name}</p>}
      <p/>

      {/* <button onClick={handleAddClick}>OK</button> */}
      <button className="button" onClick={handleAddClick}>OK</button>
      <p>{result}</p>

      {/* {showButton && (
        <button onClick={handleButtonClick}>Hiển thị kết quả</button>
      )} */}
      {showButton && (
        <button className="button" onClick={handleButtonClick}>Kết quả</button>
      )}

      {showImageComponent && <ImageComponent />}

    </div>
  );
}

function FCMParallel() {
  const [result, setResult] = useState("");
  const [showButton, setShowButton] = useState(false);

  const [showImageComponent, setShowImageComponent] = useState(false);

  const [option, setOption] = useState("");
  const handleNumberChange = (event) => {
    setOption(event.target.value);
  };

  const [selectedFile, setSelectedFile] = useState(null);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleAddClick = async () => {
    try {
      const result = await callAddAPI2(selectedFile.name, option);
      setResult(result);
      setShowButton(true);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleButtonClick = () => {
    setResult(result);
    setShowImageComponent(true);
  };

  return (
    <div>
      <h1>FCM</h1>
      <p>Lựa chọn 1: Chạy song song</p>
      <p>Lựa chọn 2: Chạy tuần tự</p>
      <p/>
      
      <input className="custom-file-input"
        type="file"
        accept=".dcm"
        onChange={handleFileChange}
      />
      {selectedFile && <p>Tên tệp đã chọn: {selectedFile.name}</p>}

      <p/>
      <select className="custom-select" value={option} onChange={handleNumberChange}>
        <option value="">Chọn option</option>
        <option value="1">1</option>
        <option value="2">2</option>
      </select>

      <p/>
      <button className="button" onClick={handleAddClick}>OK</button>
      <p>{result}</p>

      {showButton && (
        <button className="button" onClick={handleButtonClick}>Kết quả</button>
      )}

      {showImageComponent && <ImageComponent2 />}
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <Nav/>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/aboutus" element={<AboutUs />} />
        <Route path="/fcm" element={<FCM />} />
        <Route path="/fcmParallel" element={<FCMParallel />} />
      </Routes>
    </div>
  );
}

export default App;