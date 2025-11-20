# Security Guidelines

## Reporting Security Issues

If you discover a security vulnerability, please email: rodrigo.paiva@onisolucoes.net

## Security Best Practices

### Environment Variables

All sensitive information must be stored in environment variables:

- `SECRET_KEY` - Flask secret key (generate with `openssl rand -hex 32`)
- `DATABASE_URL` - Database connection string
- `ROOT_ADMIN_EMAIL` - Email for root administrator
- OpenAI API key stored in Settings model (admin panel)

### Never Commit

❌ Never commit these files:
- `.env` files
- `*.db` database files
- `*.sock` socket files
- API keys or tokens
- Private keys or certificates

### Password Security

- All passwords are hashed using `werkzeug.security`
- Use strong passwords (minimum 12 characters, mix of upper/lower/numbers/symbols)
- Admin passwords should be rotated regularly

### Database Security

- SQLite database files are gitignored
- Backup database regularly
- Use environment variables for production database URLs

### SSL/TLS

- Production deployment uses Let's Encrypt SSL certificates
- Auto-renewal configured via certbot
- All HTTP traffic redirected to HTTPS

### Access Control

- Admin panel requires `is_admin=True` flag
- Login supports username or email
- Use `@admin_required` decorator for protected routes

## Security Checklist

Before deploying:

- [ ] All `.env` files configured properly
- [ ] SECRET_KEY is randomly generated
- [ ] Database credentials are secure
- [ ] SSL certificate is valid
- [ ] Admin passwords are strong
- [ ] No hardcoded credentials in code
- [ ] .gitignore is comprehensive
- [ ] Security headers configured in Nginx
- [ ] Regular backups scheduled

## Dependency Security

Run security audits regularly:

```bash
pip install safety
safety check
```

Update dependencies:

```bash
pip list --outdated
pip install -U package-name
```

## Server Security

### Firewall Rules

Only these ports should be open:
- 22 (SSH)
- 80 (HTTP - redirects to HTTPS)
- 443 (HTTPS)

### SSH Access

- Use SSH keys only (no password authentication)
- Keep private keys secure
- Rotate keys periodically

### System Updates

```bash
sudo apt update && sudo apt upgrade -y
sudo reboot  # if kernel updated
```

## Incident Response

In case of security breach:

1. Immediately revoke all API keys
2. Reset all user passwords
3. Review access logs
4. Update all dependencies
5. Rotate SECRET_KEY
6. Notify affected users

## Compliance

- LGPD/GDPR: User data is encrypted and stored securely
- Health data: Follow applicable healthcare regulations
- Data retention: Configure appropriate retention policies
