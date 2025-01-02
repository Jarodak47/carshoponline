import { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/auth";
import Sipnner from '../admin/Spinner'

export default function AdminRoutes() {
    const [ok, setOk] = useState(false);
    const [auth] = useAuth();

    useEffect(() => {
        const authCheck = async () => {
            const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/auths/me`, {
                headers: {
                    Authorization: `Bearer ${auth?.token?.access_token}`
                }
            });
            console.log(res.data.code)
            if (res.data.ok && res.data.role.code === 'administrator') {
                setOk(true);
            } else {
                setOk(false);
            }
        };
        if (auth?.token) authCheck();
    }, [auth?.token]);

    return ok ? <Outlet /> : <Sipnner path="" />;
}