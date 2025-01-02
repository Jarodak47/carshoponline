import { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/auth";
import Sipnner from '../admin/Spinner'

export default function PrivateRoute() {
    const [ok, setOk] = useState(false);
    const [auth] = useAuth();

    useEffect(() => {
        const authCheck = async () => {
            const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/auths/me`, {
                headers: {
                    Authorization: `Bearer ${auth?.token?.access_token}`
                }
            });
            if (res.data.ok) {
                setOk(true);
            } else {
                setOk(false);
            }       
        };
        if (auth?.token?.access_token) authCheck();
    }, [auth?.token?.access_token]);

    return ok ? <Outlet /> : <Sipnner />;
}