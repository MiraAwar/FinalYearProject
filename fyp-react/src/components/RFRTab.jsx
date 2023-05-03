import React, { useState } from 'react';

const RFRTab = () => {

    const [tab, setTab] = useState(1);
    const [file, setFile] = useState(null)
    const [filename, setFilename] = useState('')
    const [apiResponse, setApiResponse] = useState('');

    function processFile(file) {
        setFile(file);
        setFilename(file.name);
        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        fetch("http://localhost:5000//upload_file", {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
    }

      
return(
    <div>
        
    </div>
)}

export default RFRTab;