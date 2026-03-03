# Site Telefonie — Django Telecom Platform

A full-featured web application for a telecommunications company, built with **Django 5.2** and **PostgreSQL**. The platform lets customers browse services, phones, and subscription packages, while staff can manage products, promotions, and users through a customized admin panel.

---

## What the App Does

The platform simulates the commercial website of a telecom operator. Visitors can browse available services (mobile, fiber internet, cable TV), phones, and subscription bundles. Registered users get a personal profile, a browsing history, and can receive targeted promotional emails based on the packages they've viewed. Staff members manage the catalog and users through a role-based admin interface.

---

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL with a database named `dj2025` and a schema named `django`
- `pip` or a virtual environment manager


---

## 📁 Project Structure

```
proiect1/                  # Django project config (settings, root urls, wsgi)
site_telefonie/            # Main app
├── models.py              # All data models
├── views.py               # All view functions
├── urls.py                # URL routing
├── admin.py               # Customized admin panels
├── forms.py               # Django forms
├── templates/
│   └── site_telefonie/    # HTML templates
├── Mesaje/                # Contact form submissions (saved as JSON)
└── static/
media/                     # Uploaded images (services, phones)
*.log                      # Log files (debug, info, warning, error, critical)
loguri.txt                 # Access log (IP, URL, timestamp)
```

---

## Data Models

### Product Hierarchy

`Produs` is the parent model for all sellable items. `Serviciu` and `Telefon` extend it via Django's multi-table inheritance.

| Model | Description |
|---|---|
| `Produs` | Base product (name, price) |
| `Serviciu` | Telecom service (mobile, fiber, cable TV) with activation fee and status |
| `Telefon` | Phone (brand, model, stock, IMEI, availability status) |

### Packages & Promotions

| Model | Description |
|---|---|
| `CategoriePachet` | Package category (e.g. Personal, Business) with minimum contract duration |
| `Pachet` | Subscription bundle — links products, a category, and an optional promotion |
| `Promotie` | Discount promotion with date range, email subject/body, and target categories (M2M) |

### Users

`UtilizatorPersonalizat` extends Django's `AbstractUser` with:

- `data_nasterii` — date of birth (validated: must be 18+)
- `adresa` — address
- `telefon` — phone number (validated: exactly 10 digits)
- `judet` — Romanian county (choices from all 41 counties + Bucharest)
- `nr_card_implicit` — default card number (validated: 16 digits)
- `cnp` — National ID number (unique)
- `blocat` — account lock flag
- `email_confirmat` — email verification flag
- `cod` — UUID token used for email confirmation



## URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `index` | Homepage |
| `/despre/` | `despre` | About page |
| `/contact/` | `contact` | Contact form |
| `/produse/` | `lista_produse` | Product listing with filters and pagination |
| `/produs/<pk>/` | `detalii_produs` | Product detail page |
| `/pachete/` | `lista_pachete` | Package listing with filters and pagination |
| `/detalii-pachet/<pk>/` | `detalii_pachet` | Package detail + view tracking |
| `/categorii/` | `lista_categorii` | All package categories |
| `/categorii/<nume>/` | `pachete_categorie` | Packages filtered by category |
| `/produse/adauga/` | `adauga_produs` | Add a new product (permission required) |
| `/inregistrare/` | `pagina_inregistrare` | User registration with email confirmation |
| `/login/` | `custom_login_view` | Login with brute-force protection |
| `/logout/` | `logout_view` | Logout |
| `/logout-custom/` | `logout_custom` | Logout + revoke special offer permission |
| `/profil_utilizator/` | `profil_utilizator` | User profile (login required) |
| `/schimbare_parola/` | `schimbare_parola` | Change password |
| `/confirmare_email/<cod>/` | `confirmare_email` | Email confirmation via UUID link |
| `/creare-promotie/` | `creare_promotie` | Create a promotion + send bulk emails |
| `/oferta/` | `oferta_view` | Special offer page (permission-gated) |
| `/claim-oferta/` | `claim_oferta` | Claim the special offer permission |
| `/log/` | `log` | Access log viewer (admin group only) |
| `/info/` | `info` | Server info (admin group only) |
| `/interzis/` | `eroare_403_view` | Custom 403 error page |

---

## Roles & Permissions

| Role / Group | Access |
|---|---|
| `Administratori_site` | Can view `/log/` and `/info/` |
| `Moderatori` | Can edit limited user fields in admin (name, email, block status only) |
| Users with `add_produs` permission | Can access `/produse/adauga/` |
| Users with `vizualizeaza_oferta` permission | Can view `/oferta/` |
| Superusers | Full admin access |

---

## Email Features

- **Registration confirmation** — sends a UUID link to verify the user's email before allowing login.
- **Admin alerts** — notifies admins if someone tries to register as `admin`, or if login fails 3+ times in the same session within 2 minutes.
- **Promotional bulk email** — when a promotion is created, emails are sent via `send_mass_mail` to users who have viewed at least 3 packages in the targeted categories. The `Business` category uses a separate email template.

> Email uses the **console backend** in development (emails print to terminal). Switch to `smtp.EmailBackend` and configure SMTP credentials for production.

---

## Logging

Logs are written to separate files by severity:

| File | Level |
|---|---|
| `debug.log` | DEBUG and above |
| `info.log` | INFO and above |
| `warning.log` | WARNING and above |
| `error.log` | ERROR and above |
| `critical.log` | CRITICAL only |

Warnings and above are also echoed to the console.

---

## Security Features

- **Brute-force login protection** — tracks failed attempts in the session; alerts admins after 3 failures within 2 minutes.
- **Account locking** — accounts flagged as `blocat` are blocked from logging in.
- **Email confirmation** — new accounts must confirm their email before they can log in.
- **403 counter** — tracks how many 403 errors a session accumulates (resets on user change). Threshold configurable via `N_MAX_403` in settings.
- **Access log** — every page visit is logged to `loguri.txt` with IP, URL, and timestamp. The `/log/` page (admin-only) supports filtering by ID list, last N entries, and table/list display modes.

---

## Admin Panel

The Django admin panel is customized with:

- A branded header ("Panou administrare")
- `PachetAdmin` — searchable and filterable list, collapsible fieldsets, horizontal M2M widget for included products
- `UtilizatorPersonalizatAdmin` — full custom fieldsets; moderators can only edit name, email, and block status; all other fields are read-only for them

---

## 👤 Author

Academic project — Django Web Technologies course  
University year 2025–2026
