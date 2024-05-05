import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function ImagePage() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [name, setName] = useState('');
    const [label, setLabel] = useState('');
    const [images, setImages] = useState([]);

    useEffect(() => {
        fetchImages();
    }, []);

    const fetchImages = async () => {
        try {
            const response = await axios.get('http://localhost:5000/images');
            setImages(response.data.images);
        } catch (error) {
            console.error('Failed to fetch images:', error);
            alert('Failed to fetch images');
        }
    };

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
                fetchImages();
            }
        } catch (error) {
            console.error('Image upload failed:', error.response ? error.response.data : 'Unknown error');
            alert('Image upload failed');
        }
    };

    const handleDeleteImage = async (imageName) => {
        try {
            const response = await axios.delete(`http://localhost:5000/image/${encodeURIComponent(imageName)}`);
            alert(JSON.stringify(response.data));
            if (response.status === 200) {
                fetchImages(); // Refresh the list after deletion
            }
        } catch (error) {
            console.error('Failed to delete image:', error.response ? error.response.data : 'Unknown error');
            alert('Failed to delete image');
        }
    };

    const handleStartTraining = async () => {
        try {
            const response = await axios.post('http://localhost:5000/training');
            if (response.status === 202) {
                navigate('/test');
            }
        } catch (error) {
            console.error('Failed to start training:', error.response ? error.response.data : 'Unknown error');
            alert('Failed to start training');
        }
    }

    return (
        <div className="image-page-container">
            <div className="image-list" style={{ overflowY: 'scroll', height: '200px' }}>
                <h2>Stored Images</h2>
                <ul>
                    {images && images.map((img) => (
                        <li key={img.name}>
                            {img.name} <span onClick={() => handleDeleteImage(img.name)} style={{ cursor: 'pointer', color: 'red' }}>✖</span>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="image-upload-form">
                <input type="file" onChange={e => setFile(e.target.files[0])} />
                <input type="text" placeholder="Enter image name" value={name} onChange={e => setName(e.target.value)} />
                <input type="text" placeholder="Enter label" value={label} onChange={e => setLabel(e.target.value)} />
                <button onClick={handleAddImage}>Upload Image</button>
            </div>
            <div style={{ textAlign: 'center', marginTop: '20px' }}>
                <button onClick={handleStartTraining}>Start Training</button>
            </div>
        </div>
    );
}

export default ImagePage;
