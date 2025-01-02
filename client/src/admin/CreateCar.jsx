import React, { useEffect, useState } from 'react';
import AdminMenu from './AdminMenu';
import axios from 'axios';
import { Select } from 'antd';
import { useNavigate } from 'react-router-dom';
import Loading from './Loading';
import toast from 'react-hot-toast';

const { Option } = Select;

const CreateCar = () => {
    const [formData, setFormData] = useState({});
    const [brands, setBrands] = useState([]);
    const [imagePreviews, setImagePreviews] = useState([]);

    const [imageFiles, setImageFiles] = useState([]);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const fetchBrands = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/brands/all`);
            if (response.data.success) {
                setBrands(response.data.data);
            }
        } catch (error) {
            console.error(error);
        }
    };

    const validateForm = () => {
        if (!formData.brand_uuid) {
            toast.error('Brand is required');
            return false;
        }
        if (!formData.model || formData.model.trim() === '') {
            toast.error('vehicle model is required');
            return false;
        }
        if (!formData.price || formData.price <= 0) {
            toast.error('Price must be a positive number');
            return false;
        }
        if (!formData.year || formData.year < 1886 || formData.year > new Date().getFullYear()) {
            toast.error('Year must be between 1886 and the current year');
            return false;
        }
        if (!formData.fuelType || formData.fuelType.trim() === '') {
            toast.error('fuelType is required');
            return false;
        }
        if (!formData.fuelTank || formData.fuelTank.trim() === '') {
            toast.error('fuelTank is required');
            return false;
        }

        if (!formData.engineSize) {
            toast.error('engineSize is required');
            return false;
        }
        if (!formData.mileage) {
            toast.error('mileage is required');
            return false;
        }
        if (!formData.safetyrating) {
            toast.error('safetyrating is required');
            return false;
        }
        if (!formData.seater) {
            toast.error('seater is required');
            return false;
        }
        if (!formData.transmission || formData.transmission.trim() === '') {
            toast.error('transmission is required');
            return false;
        }
        if (!formData.warranty) {
            toast.error('warranty is required');
            return false;
        }

        if (!formData.color || formData.color.trim() === '') {
            toast.error('Color is required');
            return false;
        }
        if (imageFiles.length === 0) {
            toast.error('Please upload at least one image');
            return false;
        }
        // Ajoutez d'autres vérifications selon vos besoins
        return true;
    };

    const handleFileChange = (event) => {
        const files = Array.from(event.target.files);
        setImageFiles(files);

        // Générer les URL de prévisualisation
        const previews = files.map(file => URL.createObjectURL(file));
        setImagePreviews((prevPreviews) => [...prevPreviews, ...previews]);
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) {
            return;
        }
        setLoading(true);
        try {
            const imageUUIDs = await Promise.all(
                imageFiles.map(async (file) => {
                    const formData = new FormData();
                    formData.append('file', file);

                    const upload_response = await axios.post(
                        `${process.env.REACT_APP_API_URL}/api/v1/storages/upload`,
                        formData,
                        { headers: { 'Content-Type': 'multipart/form-data' } }
                    );
                    if (upload_response.status!== 200) {
                        toast.error( response.detail ||'Error in uploading vehicle images');
                    }
                    return upload_response.data.uuid;
                })
            );

            const response = await axios.post(
                `${process.env.REACT_APP_API_URL}/api/v1/vehicles/create`,
                { ...formData, image_uuids: imageUUIDs }
            );
            console.log(response)

            if (response.status === 200) {
                toast.success('Car Created Successfully');
                navigate('/dashboard/admin/cars');
            } else {
                toast.error( response.detail ||'Error in Car creation');
            }
        } catch (error) {
            console.log(error);
            toast.error( error.response.data.detail ||'Error in Car creation');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchBrands();
        window.scrollTo(0, 0);
    }, []);

    return (
        <div className="container marginStyle">
            {!loading ? (
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-md-3">
                            <AdminMenu />
                        </div>
                        <div className="col-md-9 my-3">
                            <form method="post" encType="multipart/form-data" onSubmit={handleSubmit}>
                                <h1 className="text-center">Create Car</h1>
                                <div className="m-1">
                                    <Select
                                        bordered={false}
                                        placeholder="Select A Brand"
                                        size="large"
                                        showSearch
                                        className="form-select mb-3"
                                        value={formData.brand_uuid || undefined}
                                        onChange={(value) => setFormData((prev) => ({ ...prev, brand_uuid: value }))}
                                    >
                                        {brands.map((brand) => (
                                            <Option key={brand.uuid} value={brand.uuid}>
                                                {brand.name}
                                            </Option>
                                        ))}
                                    </Select>

                                    <div className="mb-3">
                                        <label className="btn btn-outline-primary col-md-12">
                                            Upload Images
                                            <input
                                                type="file"
                                                name="productPictures"
                                                accept="image/*"
                                                multiple
                                                onChange={handleFileChange}
                                                hidden
                                            />
                                        </label>
                                    </div>
                                    {/* Afficher les prévisualisations d'image */}
                                    <div className="mb-3">
                                        {imagePreviews.map((preview, index) => (
                                            <img
                                                key={index}
                                                src={preview}
                                                alt={`Preview ${index}`}
                                                style={{ maxWidth: '100px', marginRight: '10px' }}
                                            />
                                        ))}
                                    </div>

                                    {[
                                        { name: 'model', placeholder: 'Model Name',type:'text',required:true },
                                        { name: 'year', placeholder: 'Car Year',type:'number',required:true,min: 1886, max: new Date().getFullYear() },
                                        { name: 'color', placeholder: 'Car color',type:'text',required:true },
                                        { name: 'price', placeholder: 'Price (e.g., 10000)',type:'number',required:true,min: 0, step: 1 },
                                        { name: 'fuelType', placeholder: 'Fuel Type' ,type:'text',required:true},
                                        { name: 'transmission', placeholder: 'Transmission Type',type:'text',required:true },
                                        { name: 'engineSize', placeholder: 'Engine Size',type:'number',required:true,min: 0, step: 0.1 },
                                        { name: 'mileage', placeholder: 'Mileage',type:'number',required:true,min: 0, step: 1 },
                                        { name: 'safetyrating', placeholder: 'Safety Rating',type:'number',required:true,min: 0, step: 1 },
                                        { name: 'warranty', placeholder: 'Warranty',type:'number',required:true },
                                        { name: 'seater', placeholder: 'Number of Seats',min: 1, step: 1  },
                                        { name: 'size', placeholder: 'Dimensions (H x W)',type:'text',required:true },
                                        { name: 'fuelTank', placeholder: 'Fuel Tank Capacity',type:'number',required:true,min: 0, step: 0.1 },
                                    ].map(({ name, placeholder,type,required,min,max,step }) => (
                                        <div className="mb-3" key={name}>
                                            <input
                                                type={type}
                                                name={name}
                                                placeholder={placeholder}
                                                className="form-control"
                                                onChange={handleInputChange}
                                                required={required}
                                                min={min}
                                                max={max}
                                                step={step}

                                            />
                                        </div>
                                    ))}

                                    <div className="mb-3">
                                        <textarea
                                            rows={3}
                                            name="description"
                                            placeholder="Description"
                                            className="form-control"
                                            onChange={handleInputChange}
                                        />
                                    </div>
                                    {/* <div className="mb-3">
                                        <textarea
                                            rows={3}
                                            name="year"
                                            placeholder="Year"
                                            className="form-control"
                                            onChange={handleInputChange}
                                            required
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <textarea
                                            rows={3}
                                            name="color"
                                            placeholder="Color"
                                            className="form-control"
                                            onChange={handleInputChange}
                                            required
                                        />
                                    </div> */}

                                    <div className="mb-3">
                                        <Select
                                            bordered={false}
                                            placeholder="Select Shipping"
                                            size="large"
                                            showSearch
                                            className="form-select mb-3"
                                            onChange={(value) => setFormData((prev) => ({ ...prev, shipping: value }))}
                                        >
                                            <Option value="0">No</Option>
                                            <Option value="1">Yes</Option>
                                        </Select>
                                    </div>

                                    <div className="mb-3">
                                        <button className="btn btn-success" type="submit">
                                            Create Car
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            ) : (
                <Loading />
            )}
        </div>
    );
};

export default CreateCar;