import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function TestPage() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [results, setResults] = useState("");

    const handleFileUpload = (e) => {
        setFile(e.target.files[0]);
    };

    const handleTest = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:5000/inference', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResults(`Inference task submitted successfully. Inference ID: ${response.data.inference_id}`);
            // Optionally navigate or trigger additional actions
        } catch (error) {
            console.error('Error submitting inference:', error);
            setResults('Failed to submit inference.');
        }
    };

    return (
        <div className="test-page-container">
            <h1>Test</h1>
            <div className="test-controls">
                <input type="file" onChange={handleFileUpload} />
                <button onClick={handleTest}>Run Test</button>
            </div>
            <div className="results-box">
                {results}
            </div>
        </div>
    );
}

export default TestPage;
