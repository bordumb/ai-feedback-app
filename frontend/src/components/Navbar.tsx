//frontend/src/componentsNavBar.tsx
export default function Navbar() {
    return (
        <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
            <a href="/auth">Login</a> | <a href="/signup">Signup</a> | <a href="/">Home</a> | <a href="/dashboard">Dashboard</a>
        </nav>
    );
}
