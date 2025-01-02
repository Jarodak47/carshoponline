import React, { useEffect, useState } from 'react'
import UserMenu from './UserMenu'
import { useAuth } from '../context/auth'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const UserProfile = () => {
    const [auth] = useAuth();
    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [avatarUuid, setAvatar] = useState("");
    // const [roleCode,setRole] = useState("");

    // const [roles,setRoles] = useState([]);
    const [email, setEmail] = useState("");
    // const [loadingRoles, setLoadingRoles] = useState(true); // État de chargement des rôles
    const [phonenumber, setPhonenumber] = useState("");
    const [address, setAddress] = useState("");
    const [file, setFile] = useState(null);
    const navigate = useNavigate()

    // const getRoleUuid = async (roleCode) => {
    //     try {
    //         const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/roles`,{
    //             params: { code: roleCode }
    //         } );
    //         console.log(response)

    //         return response.data[0].uuid;
    //     } catch (error) {
    //         toast.error("le role n'existe pas");
    //         throw error;
    //     }
    // };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    // useEffect(() => {
    //     const fetchRoles = async () => {
    //         try {
    //             const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/roles`);
    //             setRoles(response.data);
    //             setLoadingRoles(false); // Fin du chargement des rôles
    //         } catch (error) {
    //             toast.error("Failed to fetch roles");
    //             setLoadingRoles(false); // Fin du chargement des rôles

    //         }
    //     };

    //     fetchRoles();
    // }, []);


    useEffect(() => {
        if (auth?.user) {
            // console.log(auth.user.role.code)
            const { email, firstname,lastname,avatarUuid,phonenumber, address } = auth?.user;
            setFirstname(firstname);
            setPhonenumber(phonenumber);
            setEmail(email);
            setAddress(address);
            setLastname(lastname);
            setAvatar(avatarUuid);
            window.scrollTo(0, 0)
        }
    }, [auth?.user]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (file) {
                const formData = new FormData();
                formData.append('file', file);
                const uploadResponse = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/storages/upload`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                setAvatar(uploadResponse?.data?.uuid)
            }
            // const roleUuid = await getRoleUuid(roleCode);
            const { data } = await axios.put(`${process.env.REACT_APP_API_URL}/api/v1/users`, {
                firstname,
                lastname,
                avatarUuid,
                uuid:auth?.user.uuid,
                // role_uuid:roleUuid,
                email,
                phonenumber,
                address,
            });
            if (data?.error) {
                toast.error(data?.error);
            } else {
                // setAuth({ ...auth, user: data?.updatedUser });
                let ls = localStorage.getItem("auth");
                ls = JSON.parse(ls);
                ls.user = data.updatedUser;
                localStorage.setItem("auth", JSON.stringify(ls));
                toast.success("Profile Updated Successfully");
                navigate('/')
            }
        } catch (error) {
        }
    };
    return (
        <div className='container marginStyle'>
            <div className='container-fluid'>
                <div className='row'>
                    <div className='col-md-3'>
                        <UserMenu />
                    </div>
                    <div className='col-md-9 my-3'>
                        <h3 className='text-center'>Update Profile</h3>
                        <div className="card text-black mb-5">
                            <div className="card-body p-md-5">
                                <div className="row justify-content-center">
                                    <form className="mx-1 mx-md-4" onSubmit={handleSubmit}>
                                        <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="firstname">First Name</label>
                                            <input value={firstname} onChange={(e) => setFirstname(e.target.value)} type="text" id="firstname" className="form-control" />
                                        </div>
                                        <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="lastname">Last Name</label>
                                            <input value={lastname} onChange={(e) => setLastname(e.target.value)} type="text" id="lastname" className="form-control" />
                                        </div>
                                        <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="email">Email</label>
                                            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" id="email" className="form-control" />
                                        </div>
                                        <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="phonenumber">Phone Number</label>
                                            <input value={phonenumber} onChange={(e) => setPhonenumber(e.target.value)} type="text" id="phonenumber" className="form-control" />
                                        </div>
                                        
                                        <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="address">Address</label>
                                            <input value={address} onChange={(e) => setAddress(e.target.value)} type="text" id="address" className="form-control" />
                                        </div>

                                        {/* <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="role">Role</label>
                                            <select value={roleCode} onChange={(e) => setRole(e.target.value)} id="role" className="form-control">
                                            <option value="">Select Role</option>
                                                {loadingRoles ? (
                                                    <option disabled>Loading roles...</option>
                                                ) : (
                                                    roles.map((role) => (
                                                        <option key={role.code} value={role.code}>
                                                            {role.code}
                                            </option> ))
                                                )}
                                        
                                            </select>

                                        </div> */}
                                        <div className="form-group mb-4">
                                            <label className="form-label" htmlFor="file">Upload Avatar</label>
                                            <input type="file" id="file" className="form-control" onChange={handleFileChange} />
                                        </div>
                                        <button type="submit" className="btn btn-primary">Update Profile</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserProfile
