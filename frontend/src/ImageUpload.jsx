import React, { useState } from "react";

import { Dropzone, FileItem } from "@dropzone-ui/react";

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

  const onSubmit = async() =>{
    
  }

  return (
    <>
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
                  <FileItem
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
            <button className="button" onClick={onSubmit}>Know what it is?</button>
          </div>
        </div>
      </div>
    </>
  );
}

export default ImageUpload;
