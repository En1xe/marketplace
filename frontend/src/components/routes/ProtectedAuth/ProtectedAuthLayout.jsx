import { Outlet } from "react-router-dom";

import ProtectedAuthRoute from "./ProtectedAuthRoute";


export default function ProtectedAuthLayout() {
    return (
        <ProtectedAuthRoute>
            <Outlet />
        </ProtectedAuthRoute>
    )
}