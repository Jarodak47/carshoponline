import React, { useEffect, useState } from 'react'
import AdminMenu from './AdminMenu'
import axios from 'axios'
import { Link } from 'react-router-dom';
import { BsFuelPumpFill } from 'react-icons/bs'
import { PiCurrencyInrFill } from 'react-icons/pi'
import toast from 'react-hot-toast';
import { ColorRing } from 'react-loader-spinner'

const Cars = () => {

    const [cars, setcars] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [carToDelete, setCarToDelete] = useState(null);


    const getAllcars = async () => {
        try {
            const data = await fetch(`${process.env.REACT_APP_API_URL}/api/v1/vehicles/all`, {
                method: "GET",
                headers: { "Content-type": "application/json" }
            })
            const data_ = await data.json()
            setcars(data_.data.reverse())
            setLoading(false);
        } catch (error) {
            console.log(error);
            setLoading(true);
        }
    };
    const showDeleteConfirm = (id) => {
        setCarToDelete(id);
        setIsModalVisible(true);
    };


    const handleDelete = async (id) => {
        try {
            const { data } = await axios.delete(`${process.env.REACT_APP_API_URL}/api/v1/vehicles/${id}`)
            if (data?.message) {
                toast.success('Car Deleted Successfully')
                getAllcars()
            } else {
                toast.error('Error in Deleting car')
            }
        } catch (err) {
            console.log(err)
        } finally {
            setIsModalVisible(false);
            setCarToDelete(null);
        }
    }

    useEffect(() => {
        getAllcars();
        window.scrollTo(0, 0)
    }, []);

    return (
        <div className='container marginStyle'>
            <div className='container-fluid'>
                <div className='row'>
                    <div className='col-md-3'>
                        <AdminMenu />
                    </div>
                    <div className="col-md-9">
                        <h1 className="text-center my-3">All Cars List</h1>
                        {loading ?
                            <div className="h-100 d-flex align-items-center justify-content-center">
                                <ColorRing
                                    visible={true}
                                    colors={['#000435', 'rgb(14 165 233)', 'rgb(243 244 246)', '#000435', 'rgb(14 165 233)']}
                                />
                            </div>
                            :
                            <div className="row" style={{ marginTop: '0px' }}>
                                {cars.map((p) => (
                                    <div className="col-md-12 col-lg-4 mb-lg-0 my-3">
                                        <div className="card">
                                            <div className="d-flex justify-content-between p-3">
                                                <p className="lead mb-0">{p.brand.name}</p>
                                                <div
                                                    className=" rounded-circle d-flex align-items-center justify-content-center shadow-1-strong"
                                                    style={{ width: '40px', height: '40px' }}>
                                                    <Link to={`/brand/${p.brand.name}`} className="text-white mb-0 small">
                                                        <img src={p.brand.brandPictures} alt={p.brand.name} style={{ maxWidth: '100%', maxHeight: '150px', objectFit: 'contain' }} />
                                                    </Link>
                                                </div>
                                            </div>
                                            <Link to={`/dashboard/admin/car/${p.slug}`} className='text-center '>
                                                <img className='border rounded' src={p.productPictures[0]} alt={p.model} style={{ maxWidth: '100%', maxHeight: '100px', objectFit: 'contain' }} />
                                            </Link>
                                            <div className="card-body">
                                                <h4 className="text-center mb-4">{p.name}</h4>
                                                <div className="d-flex justify-content-between">
                                                    <h6><PiCurrencyInrFill /> : {p.price} $</h6>
                                                    <h6 ><BsFuelPumpFill /> : {p.fuelType}</h6>
                                                </div>
                                                <div className='text-center my-2'>
                                                    <Link className='btn mt-2 text-white' to={`/car/${p.slug}`} style={{ backgroundColor: 'blueviolet' }}>View</Link>
                                                    <Link to={`/dashboard/admin/car/${p.slug}`} className='btn btn-primary mt-2 mx-2'>Update</Link>
                                                    <button onClick={() => showDeleteConfirm(p.uuid)} className='btn btn-danger mt-2'>Delete</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        }
                    </div>
                </div>
                
            </div>
            {/* Modal de confirmation */}
            {isModalVisible && (
                <div className="modal" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Confirm Deletion</h5>
                                <button type="button" className="close" onClick={() => setIsModalVisible(false)}>
                                    <span>&times;</span>
                                </button>
                            </div>
                            <div className="modal-body">
                                <p>Are you sure you want to delete this car?</p>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" onClick={() => setIsModalVisible(false)}>Cancel</button>
                                <button type="button" className="btn btn-danger" onClick={() =>handleDelete(carToDelete)}>Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div >
    )
}

export default Cars
