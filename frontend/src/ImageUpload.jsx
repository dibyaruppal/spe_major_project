import React, { useState } from "react";

import { Dropzone, FileMosaic } from "@dropzone-ui/react";

import axios from "axios";
import Gauge from "./Gauge";

function ImageUpload() {
  const [files, setFiles] = useState([]);
  const [imageSrc, setImageSrc] = useState(undefined);
  const updateFiles = (incommingFiles) => {
    console.log("incomming files", incommingFiles);
    setFiles(incommingFiles);
  };
  const onDelete = (id) => {
    setFiles(files.filter((x) => x.id !== id));
  };

  const [Response, setResponse] = useState(null);
  const onSubmit = async () => {
    if (files.length > 0) {
      const formData = new FormData();
      formData.append("image", files[0].file);

      try {
        const response = await axios.post(
          "http://192.168.49.2:30007/predict",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log("File uploaded successfully:", response.data);
        setResponse(response.data);
        // Handle the response data as needed
      } catch (error) {
        console.error("Error uploading file:", error);
        // Handle the error as needed
      }
    } else {
      console.error("No files selected for upload.");
    }
  };

  return (
    <>
      {Response ? (
        <div className="centered-container">
          <div className="centered-content">
            <div className="card">
              {Response.prediction_class === "AI Generated Image" && (
                <>
                  <h1 style={{textAlign:"center"}}>AI Generated Image</h1>
                  <Gauge value={Response.predicted_probabilities[0][0]} />
                </>
              )}
              {Response.prediction_class === "Real Image" && (
                <>
                  <h1 style={{textAlign:"center"}}>Real Image</h1>
                  <Gauge value={Response.predicted_probabilities[0][1]} />
                </>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="centered-container">
          <div className="centered-content">
            <div className="card">
              <h1>Real vs AI Generated Image Detection</h1>
              <Dropzone
                style={{ minWidth: "850px" }}
                onChange={updateFiles}
                minHeight="195px"
                value={files}
                maxFiles={1}
                maxFileSize={10000000}
                accept=".png,image/*"
                uploadingMessage={"Uploading..."}
              >
                {files.length > 0 &&
                  files.map((file) => (
                    <FileMosaic
                      {...file}
                      key={file.id}
                      onDelete={onDelete}
                      //localization={"ES-es"}
                      resultOnTooltip
                      preview
                      info
                      hd
                    />
                  ))}
              </Dropzone>
            </div>
            <div className="button-container">
              <button className="button" onClick={onSubmit}>
                Know what it is?
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default ImageUpload;
