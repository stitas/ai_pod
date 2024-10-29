import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import '../styles/gallery.css'
import { useNavigate } from 'react-router-dom';

function InfiniteImageGallery({url}) {
  const serverUrl = import.meta.env.VITE_SERVER_URL;
  const navigate = useNavigate()

  const [images, setImages] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);

  const observer = useRef();

  // Function to load images from the server
  const loadImages = async () => {
    setLoading(true);
    try {
      const response = await axios.get(serverUrl + url, {
          params: { page, per_page: 20 }, // Use page and items per page
        },
      );

      // If not authorized
      if(response.status === 401){
        navigate('/login')
      }

      setImages(prevImages => [...prevImages, ...response.data.images]);
      setHasMore(response.data.has_next); // Use `has_next` to determine if more pages are available
    } catch (error) {
      console.error('Error loading images:', error);
    }
    setLoading(false);
  };

  // Infinite scroll observer
  const lastImageRef = useCallback(node => {
    if (loading) return;

    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        setPage(prevPage => prevPage + 1); // Go to the next page
      }
    });
    if (node) observer.current.observe(node);
  }, [loading, hasMore]);

  const goToProductList = (imageId) => {
    navigate(
      '/product-list',
      {
        state: { imageId: imageId  },
      }
    )
  }

  // Load initial images and update on page change
  useEffect(() => {
    loadImages();
  }, [page]);

  return (
    <div className="image-gallery">
      {images.map((image, index) => {
        if (images.length === index + 1) {
          return (
            <div className="gallery-item" onClick={() => {goToProductList(image.id)}} ref={lastImageRef}>
              <img className="image-card" src={image.url}/>
              <p className="image-description">{image.prompt}</p>
            </div>
          );
        } else {
          return (
            <div className="gallery-item" onClick={() => {goToProductList(image.id)}}>
              <img className="image-card" src={image.url} />
              <p className="image-description">{image.prompt}</p>
            </div>
          );
        }
      })}

      {/* Loading Indicator */}
      {loading && <p>Loading more images...</p>}
    </div>
  );
}

export default InfiniteImageGallery;