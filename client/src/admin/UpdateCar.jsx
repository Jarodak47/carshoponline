import React, { useEffect, useState } from 'react'
import AdminMenu from './AdminMenu'
import axios from 'axios'
import { Link, useNavigate, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'

const UpdateCar = () => {

    const params = useParams()
    const [value, setValue] = useState({})

    const navigate = useNavigate();

    const getSingleProduct = async () => {
        try {
            const { data } = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/vehicles/one/${params.slug}`)
            setValue(data)
        } catch (err) {
            console.log(err)
        }
    }
    

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {

            const { data } = await axios.put(`${process.env.REACT_APP_API_URL}/api/v1/vehicles`, value)
            console.log(data)
            
                toast.success('Car Updated Successfully')
                navigate('/dashboard/admin/cars')
           
        } catch (err) {
            console.log(err)
        }
    }

    const handleChange = (e)=>{
        return setValue({
            ...value,
            [e.target.name]: e.target.value
        })
    }
    const handleDelete = async () => {
        try {
            await axios.delete(`${process.env.REACT_APP_API_URL}/api/v1/vehicles/${value.uuid}`)
            toast.success('Car Deleted Successfully')
            navigate('/dashboard/admin/cars')
        } catch (err) {
            console.log(err)
        }
    }

    useEffect(() => {
        getSingleProduct();
        window.scrollTo(0, 0)
    }, [])

    return (
        <div className='container marginStyle'>
            <div className='container-fluid'>
                <div className='row'>
                    <div className='col-md-3'>
                        <AdminMenu />
                    </div>
                    <div className='col-md-9 my-3'>
                        <h1 className='text-center'>Update Vehicle</h1>
                        <div className='m-1'>
                            <div className='mb-3'>
                                <input type='text' value={value.model} name='model' placeholder='write a car Name' className='form-control' onChange={(e) => handleChange(e)}required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.price} name='price' placeholder='write a car Price' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.fuelType} name='fuelType' placeholder='write a car Fuel Type' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.transmission} name ='transmission' placeholder='write a car Transmission' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.engineSize} name = 'engineSize' placeholder='write a car EngineSize' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.mileage} name = 'mileage' placeholder='write a car Mileage' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.safetyrating} name = 'safetyrating' placeholder='write a car Safetyrating' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.warranty} name = 'warranty' placeholder='write a car Warranty' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.seater} name = 'seater' placeholder='write a car Seater' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.size} name = 'size' placeholder='write a car Size' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <input type='text' value={value.fuelTank} name = 'fuelTank' placeholder='write a car FuelTank' className='form-control' onChange={(e) => handleChange(e)} required />
                            </div>
                            <div className='mb-3'>
                                <textarea rows={3} type='text' value={value.description} name = 'description' placeholder='write a car Description' className='form-control' onChange={(e) => handleChange(e)} />
                            </div>
                            <div className='mb-3'>
                                <button className='btn btn-success mx-2' onClick={handleSubmit}>Update Vehicle</button>
                                <button className='btn btn-danger' onClick={handleDelete}>Delete vehicle</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    )
}

export default UpdateCar
