-- database/schemas/accounts.sql

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL CHECK (email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),
    hashed_password TEXT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),  -- Optional PII
    profile_picture TEXT,
    bio TEXT,

    -- ✅ GDPR Compliance Fields
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,   -- Soft delete mechanism
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    role VARCHAR(50) NOT NULL DEFAULT 'user',

    -- ✅ GDPR Consent & Logging
    consent_given_at TIMESTAMP WITH TIME ZONE,  -- When user accepted T&C
    consent_withdrawn_at TIMESTAMP WITH TIME ZONE,  -- When user revoked consent
    deleted_at TIMESTAMP WITH TIME ZONE,  -- Soft delete (GDPR compliance)
    export_token TEXT UNIQUE,  -- Token for exporting user data

    -- ✅ Security & Auditing
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,

    -- ✅ Encryption Fields (if needed)
    email_hash TEXT UNIQUE,  -- Store email hash for lookup without exposing raw email
    phone_hash TEXT UNIQUE   -- Store hashed phone number (if required)

);
