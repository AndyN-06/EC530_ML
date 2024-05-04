import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function HomePage() {
    const [projects, setProjects] = useState([]);
    const [project_name, setNewProjectName] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await axios.get('http://localhost:5000/projects');
                if (response.data.success) {
                    setProjects(response.data.projects);
                } else {
                    throw new Error('Failed to fetch projects');
                }
            } catch (error) {
                console.error('Failed to fetch projects:', error);
                alert('Failed to fetch projects');
                setProjects([]);
            }
        };

        fetchProjects();
    }, []);

    const handleNewProject = async(e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:5000/projects', {
                project_name,
            });
            if (response.data && response.status === 201) {
                alert(JSON.stringify(response.data));
                const newProject = response.data.name;
                setProjects(currentProjects => [...currentProjects, newProject]);
                setNewProjectName('');
            } else {
                throw new Error('Project creation unsuccessful');
            }
        } catch (error) {
            console.error('New Project failed:', error.response ? error.response.data : 'Unknown error');
            alert('Failed to Create New Project');
        }
    };

    return (
        <div className="homepage-container">
            <h1>Projects</h1>
            <div className="projects-list">
                {projects && projects.map(project => (
                    <div key={project.name} className="project-item" onClick={() => navigate('/project')}>
                        {project.name}
                    </div>
                ))}
            </div>
            <form onSubmit={handleNewProject}>
                <input
                    value={project_name}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    placeholder="Enter new project name"
                />
                <button type="submit">Create New Project</button>
            </form>
        </div>
    );
}

export default HomePage;
