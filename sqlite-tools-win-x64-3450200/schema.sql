-- Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    active INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- Projects Table
CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('classification', 'object_detection')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Datasets (
    dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

-- Images Table
CREATE TABLE Images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    image BLOB NOT NULL,
    label TEXT,
    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

-- Labels Table
CREATE TABLE Labels (
    label_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

-- Image_Labels Table
CREATE TABLE Image_Labels (
    image_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    PRIMARY KEY (image_id, label_id),
    FOREIGN KEY (image_id) REFERENCES Images(image_id),
    FOREIGN KEY (label_id) REFERENCES Labels(label_id)
);

-- Training Sessions Table
CREATE TABLE Training (
    training_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    start_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    status TEXT NOT NULL,
    training_result INTEGER,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Configurations (
    configuration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    value INTEGER,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

-- Models Table
CREATE TABLE Models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    model_file_path TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES Training_Sessions(session_id)
);

-- Inferences Table
CREATE TABLE Inferences (
    inference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    result TEXT,
    inferred_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES Models(model_id),
    FOREIGN KEY (image_id) REFERENCES Images(image_id)
);

-- Test Model Table
CREATE TABLE Tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    test_results TEXT,
    tested_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES Models(model_id)
);

-- Reports Table
CREATE TABLE Reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    report_content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES Training_Sessions(session_id)
);