import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function ImagePage() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [name, setName] = useState('');
    const [label, setLabel] = useState('');
    const [imageNames, setImageNames] = useState([]);

    // Moved fetchImages outside of useEffect to make it accessible elsewhere
    const fetchImages = async () => {
        try {
            const response = await axios.get('http://localhost:5000/images');
            setImageNames(response.data.images);
        } catch (error) {
            console.error('Failed to fetch images:', error);
            alert('Failed to fetch images');
        }
    };

    useEffect(() => {
        fetchImages();
    }, []);

    const handleAddImage = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', name);
        formData.append('label', label);
        try {
            const response = await axios.post('http://localhost:5000/upload/train', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            alert(JSON.stringify(response.data));
            if (response.status === 200 || response.status === 201) {
                fetchImages(); // Call fetchImages to refresh the list after uploading
            }
        } catch (error) {
            console.error('Image upload failed:', error.response ? error.response.data : 'Unknown error');
            alert('Image upload failed');
        }
    };

    return (
        <div className="image-page-container">
            <div className="image-list">
                <h2>Stored Images</h2>
                <ul>
                    {imageNames && imageNames.map((img, index) => (
                        <li key={index}>{img}</li>
                    ))}
                </ul>
            </div>
            <div className="image-upload-form">
                <input type="file" onChange={e => setFile(e.target.files[0])} />
                <input type="text" placeholder="Enter image name" value={name} onChange={e => setName(e.target.value)} />
                <input type="text" placeholder="Enter label" value={label} onChange={e => setLabel(e.target.value)} />
                <button onClick={handleAddImage}>Upload Image</button>
            </div>
        </div>
    );
}

export default ImagePage;
