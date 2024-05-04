import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function ProjectPage() {
    const navigate = useNavigate();

    const handleGoToImage = () => {
        navigate('/image');
    };

    const handleGoToTest = () => {
        navigate('/test');
    };

    return (
        <div className="project-page-container">
            <h1>Project Page</h1>
            <div className="buttons-container">
                <button onClick={handleGoToImage}>New Model</button>
                <button onClick={handleGoToTest}>Test Model</button>
            </div>
        </div>
    );
}

export default ProjectPage;
