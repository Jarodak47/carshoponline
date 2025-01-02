import React, { useEffect, useState } from 'react';
import AdminMenu from './AdminMenu';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Loading from './Loading'
import toast from 'react-hot-toast';

const CreateBrands = () => {
    const [name, setFirstname] = useState('');
    const [brandPicture, setBrandPicture] = useState([]);
    const [preview, setPreview] = useState(null); // État pour l'aperçu de l'image
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    
    
    const validateForm = () => {
        if (!name.trim()) {
            toast.error('Brand name is required');
            return false;
        }
        if (!brandPicture || brandPicture.length === 0) {
            toast.error('Please upload a brand image');
            return false;
        }
        return true;
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setBrandPicture(file);
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setPreview(imageUrl); // Mettre à jour l'aperçu de l'image
        } else {
            setPreview(null); // Réinitialiser l'aperçu si aucun fichier n'est sélectionné
        }
    };


    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        if (!validateForm()) {
            setLoading(false);
            return;
        }
        try {
            const formData = new FormData();
            formData.append('file', brandPicture);

            const response = await axios.post(
                `${process.env.REACT_APP_API_URL}/api/v1/storages/upload`,
                formData,
                { headers: { 'Content-Type': 'multipart/form-data' } }
            );

            const imageUUID = response.data.uuid;

            const brandData = {
                name,
                logo_uuid: imageUUID
            };

            const brandResponse = await axios.post(
                `${process.env.REACT_APP_API_URL}/api/v1/brands/create`,
                brandData
            );

            if (brandResponse.data.success) {
                toast.success('Brand Created Successfully');
                navigate('/dashboard/admin/allbrands');
            } else {
                toast.error(brandResponse?.detail || 'Error in Brand creation');
            }
        } catch (error) {
            console.error(error);
            toast.error(error.response?.data?.detail || 'Error in Brand creation');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])

    return (
        <div className='container marginStyle'>
            {!loading ? (
                <div className='container-fluid'>
                    <div className='row'>
                        <div className='col-md-3'>
                            <AdminMenu />
                        </div>
                        <div className='col-md-9 my-3'>
                            <form method='post' enctype="multipart/form-data">
                                <h1 className='text-center'>Create Brand</h1>
                                <div className='m-1'>
                                    <div className='mb-3'>
                                        <input
                                            type='text'
                                            value={name}
                                            placeholder='write the brand name'
                                            className='form-control'
                                            onChange={(e) => setFirstname(e.target.value)}
                                            required
                                        />
                                    </div>
                                    <div className='mb-3'>
                                        <label className='btn btn-outline-primary col-md-12'>
                                            Upload Brand Image
                                            <input
                                                type='file'
                                                name='brandPicture'
                                                accept='image/*'
                                                onChange={handleFileChange}
                                                hidden
                                            />
                                        </label>
                                    </div>
                                    {preview && (
                                        <div className='mb-3 text-center'>
                                            <img
                                                src={preview}
                                                alt='Aperçu de la marque'
                                                style={{ maxWidth: '100%', maxHeight: '300px' }}
                                            />
                                        </div>
                                    )}
                                    <div className='mb-3'>
                                        <button className='btn btn-success' onClick={handleSubmit}>
                                            Create Brand
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            ) : <Loading />}
        </div>
    );
};

export default CreateBrands;
