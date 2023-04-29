import React, { useState } from "react";
import "./FileUpload.css";

function FileUpload(props) {
  const [childValue, setChildValue] = useState(false);

  function handleFileChange() {
    console.log("changing");
    const fileInput = document.getElementById('file-input');
    const submitButton = document.getElementById('submit-button');

    if (fileInput.files.length > 0) {
      console.log("not disab");
      submitButton.removeAttribute('disabled');
    } else {
      console.log("disab");
      submitButton.setAttribute('disabled', true);
    }    
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Do something with the file
    console.log("uploading");
    setChildValue(true);
    props.setSharedState(true);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>File:</label>
        <input type="file" id="file-input" accept="text/csv" onChange={handleFileChange} />
      </div>
      <button type="submit" id="submit-button" disabled>Process file</button>
    </form>
  );
};

export default FileUpload;
