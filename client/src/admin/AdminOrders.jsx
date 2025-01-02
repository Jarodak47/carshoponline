import React, { useEffect, useState } from 'react'
import AdminMenu from './AdminMenu'
import { useAuth } from '../context/auth'
import moment from 'moment'
import axios from 'axios'
import { Select } from "antd";
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
const { Option } = Select;

const AdminOrders = () => {
    const [status, setStatus] = useState(["PROCESSED", "PROCESSING", "NOT_PROCESSED", "DELIVERED", "CANCEL","SHIPPED"]);
    const [order, setOrder] = useState([])
    const [auth, setAuth] = useAuth()

    const getOrders = async () => {
        try {
            const { data } = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/payments/orders`)
            setOrder(data)
        } catch (err) {
            toast.error('Server Error')
        }
    }

    useEffect(() => {
        if (auth?.token) getOrders()
        window.scrollTo(0, 0)
    }, [auth?.token])

    const handleChange = async (orderId, value) => {
        try {
            const { data } = await axios.put(`${process.env.REACT_APP_API_URL}/api/v1/payments/order-status/${orderId}?status=${value}`);
            getOrders();
            toast.success(`Order Changed to ${value}`)
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className='container marginStyle'>
            <div className='container-fluid'>
                <div className='row'>
                    <div className='col-md-3'>
                        <AdminMenu />
                    </div>
                    <div className="col-md-9 my-3">
                        <h1 className="text-center">Manage Orders</h1>
                        {order?.map((o, i) => {
                            return (
                                <>
                                    <div className="table-responsive">
                                        <table className="table table-bordered text-center">
                                            <thead className='table-dark'>
                                                <tr>
                                                    <td scope="col">Id</td>
                                                    <td scope="col">Status</td>
                                                    <td scope="col">Buyer</td>
                                                    <td scope="col"> date</td>
                                                    <td scope="col">Payment</td>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <th>{i + 1}</th>
                                                    <th>
                                                        <Select
                                                            bordered={false}
                                                            onChange={(value) => handleChange(o.uuid, value)}
                                                            defaultValue={o?.status}
                                                            className=''
                                                        >
                                                            {status.map((s, i) => (
                                                                <Option key={i} value={s}>
                                                                    {s}
                                                                </Option>
                                                            ))}
                                                        </Select>
                                                    </th>
                                                    <th>{o?.buyer?.firstname}</th>
                                                    <th>{o.date_added? moment(o.date_added).fromNow(): 'Date non disponible'}</th>
                                                    <th>
                                                        <span className="badge text-bg-success">{o?.payment.status ? "Success" : "Failed"}</span>
                                                    </th>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div className="container">
                                        {o?.products?.map((p, i) => (
                                            <div className="row my-2 p-3 card flex-row text-center" key={p.uuid}>
                                                <div className="col-md-4">
                                                    <Link to={`/car/${p.slug}`} className='text-center'>
                                                        <img
                                                            src={`${process.env.REACT_APP_API_URL}/api/v1/storages/${p.brand.publicPicture_id}/get`}
                                                            style={{ maxWidth: '100%', maxHeight: '100px', objectFit: 'contain' }}
                                                            alt={p.name}
                                                        />
                                                    </Link>
                                                </div>
                                                <div className="col-md-8 ">
                                                    <p>{p.model}</p>
                                                    <p>$ {p.price} </p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </>
                            )
                        })}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default AdminOrders
