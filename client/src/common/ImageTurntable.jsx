import React, { useState, useEffect, useRef } from 'react';

const ImageTurntable = ({ images, className, style }) => {
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const intervalRef = useRef(null);

    useEffect(() => {
        startAutoPlay();
        return () => stopAutoPlay();
    }, []);

    const startAutoPlay = () => {
        intervalRef.current = setInterval(() => {
            setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
        }, 100); // Change l'image toutes les 100 millisecondes
    };

    const stopAutoPlay = () => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }
    };

    const handleMouseEnter = () => {
        stopAutoPlay();
    };

    const handleMouseLeave = () => {
        startAutoPlay();
    };

    const handleMouseMove = (e) => {
        const { width, left } = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - left;
        const newIndex = Math.floor((x / width) * images.length);
        setCurrentImageIndex(newIndex);
    };

    return (
        <div
            className={className}
            style={style}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onMouseMove={handleMouseMove}
        >
            <img src={images[currentImageIndex]} alt="3D view" className="img-fluid" />
        </div>
    );
};

export default ImageTurntable;