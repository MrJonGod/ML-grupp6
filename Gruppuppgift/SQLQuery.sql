CREATE DATABASE IF NOT EXISTS ml_project;
USE ml_project;

-- Create the 'news' table with a UNIQUE constraint on 'link'
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    summary TEXT NOT NULL,
    link VARCHAR(500) NOT NULL UNIQUE,  -- Ensures no duplicate articles
    published DATETIME NOT NULL,
    topic JSON NOT NULL
);

-- Create the 'category_counts' table to store category statistics
CREATE TABLE IF NOT EXISTS category_counts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL UNIQUE,
    article_count INT NOT NULL
);
