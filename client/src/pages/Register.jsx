import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Link, useNavigate } from 'react-router-dom';
import register from '../images/register.png'
import toast from 'react-hot-toast';
import '../styles/hero.css'

const Register = () => {
    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [roleUuid, setRoleUuid] = useState("");
    const [roleCode] = useState("user"); // Utiliser le code du rôle pour récupérer l'UUID
    // const [avatarFile, setAvatarFile] = useState(null);

    // const [avatarUuid, setAvatarUuid] = useState("");

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [phonenumber, setPhonenumber] = useState("");
    
    const [address, setAddress] = useState("");
    const navigate = useNavigate()

    const validateEmail = (email) => {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailPattern.test(email);
    };

    const getRoleUuid = async (roleCode) => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/roles`,{
                params: { code: roleCode }
            } );
            return response.data[0].uuid;
        } catch (error) {
            toast.error("le role n'existe pas");
            throw error;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validateEmail(email)) {
            toast.error('Invalid Email Format');
            return false;
        }
        try {
            const roleUuid = await getRoleUuid(roleCode);
            const res = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/users/register`,
                {email, 
                    firstname, 
                    lastname, 
                    role_uuid: roleUuid, 
                    password, 
                    phonenumber, 
                    address
            });
            if (res.data.success) {
                toast.success(res.data.message)
                navigate('/login')
            }
            if (!firstname.trim()) {
                toast.error('Name is required');
                return false;
            }
            if (!email.trim()) {
                toast.error('Email is required');
                return false;
            }
            if (!password.trim()) {
                toast.error('Password is required');
                return false;
            }
            if (!phonenumber.trim()) {
                toast.error('Phone Number is required');
                return false;
            }
            if (!address.trim()) {
                toast.error('Address is required');
                return false;
            }
        } catch (err) {
            toast.error('Server Error')
        }
    }

    useEffect(() => {
        window.scrollTo(0, 0)
    }, []);

    return (
        <div>
            <div className='marginStyle'>
                <div class="container d-flex justify-content-center align-items-center">
                    <div class="row border rounded-5 p-3 bg-white shadow box-area reverseCol">
                        <div class="col-md-6 rounded-4 d-flex justify-content-center align-items-center flex-column left-box">
                            <div class="featured-image mb-3 animateImg">
                                <img src={register} class="img-fluid" width={500} />
                            </div>
                        </div>
                        <div class="col-md-6 right-box">
                            <div class="row align-items-center">
                                <div class="header-text mb-4">
                                    <h2>Welcome</h2>
                                    <p>Your Dream Car is Waiting !</p>
                                </div>
                                <div class="input-group d-flex  align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={firstname} onChange={(e) => setFirstname(e.target.value)} placeholder='Your firstname' required type="text" class="form-control" />
                                    </div>
                                </div>
                                <div class="input-group d-flex  align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={lastname} onChange={(e) => setLastname(e.target.value)} placeholder='Your lastname' required type="text" class="form-control" />
                                    </div>
                                </div>
                                <div class="input-group d-flex flex-row align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={email} onChange={(e) => setEmail(e.target.value)} required type="email" placeholder='Your email ID' class="form-control " />
                                    </div>
                                </div>
                                <div class="input-group d-flex flex-row align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={roleUuid} onChange={(e) => setRoleUuid(e.target.value)} required type="hidden" class="form-control "  />  
                                    </div>
                                </div>
                                <div class="input-group d-flex flex-row align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={password} onChange={(e) => setPassword(e.target.value)} required type="password" placeholder='Your password' class="form-control " />
                                    </div>
                                </div>
                                <div class="input-group d-flex flex-row align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={phonenumber} onChange={(e) => setPhonenumber(e.target.value)} type="number" required placeholder='Your phonenumber number' class="form-control " />
                                    </div>
                                </div>
                                <div class="input-group d-flex flex-row align-items-center mb-3">
                                    <div class="form-outline flex-fill mb-0">
                                        <input value={address} onChange={(e) => setAddress(e.target.value)} type="text" required placeholder='Your address' class="form-control" />
                                    </div>
                                </div>
                                <div class="d-flex flex-row align-items-center mt-4 ">
                                    <div class="form-outline flex-fill mb-0">
                                        <button class="btn btn-lg  text-white" type="button" onClick={handleSubmit} style={{ backgroundColor: 'blueviolet', width: '100%' }} >Register</button>
                                    </div>
                                </div>
                                <div class="d-flex flex-row align-items-center my-3 ">
                                    <div class="form-outline flex-fill mb-0 " >
                                        <Link to='/login' class="btn btn-outline-dark btn-lg btn-block" style={{ width: '100%' }} type="button">Login</Link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div >
            </div >
        </div>
    )
}

export default Register
