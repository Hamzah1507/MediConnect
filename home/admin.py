# home/admin.py
from django.contrib import admin
from django.db import models
from .models import SignupUser, Medicine, Cart, CheckoutDetails

# Admin branding
admin.site.site_header = "MediConnect Admin"
admin.site.site_title = "MediConnect"
admin.site.index_title = "Site administration"


def choose_fields_for_admin(model, prefer=(), max_fields=4):
    """
    Safe list_display chooser: always include 'pk', then preferred names if present,
    then fallback to first concrete fields.
    """
    meta = model._meta
    field_names = {f.name for f in meta.get_fields() if getattr(f, "concrete", False)}
    chosen = ["pk"]
    for name in prefer:
        if name in field_names and name not in chosen:
            chosen.append(name)
        if len(chosen) >= max_fields:
            break
    if len(chosen) < max_fields:
        for f in meta.concrete_fields:
            if f.name not in chosen:
                chosen.append(f.name)
            if len(chosen) >= max_fields:
                break
    return tuple(chosen)


def find_text_field_on_model(model):
    """
    Return the name of a good text-like field for a model (email, username, name, title,
    or the first CharField/TextField). Returns None if none found.
    """
    # common preferred names in order
    preferred = ("email", "username", "name", "title", "label")
    for p in preferred:
        try:
            f = model._meta.get_field(p)
            # ensure it's a text-like field or email
            if isinstance(f, (models.CharField, models.TextField, models.EmailField)):
                return p
        except Exception:
            pass

    # fallback: first CharField/TextField on model
    for f in model._meta.get_fields():
        if getattr(f, "concrete", False) and isinstance(f, (models.CharField, models.TextField, models.EmailField)):
            return f.name

    return None


def build_safe_search_fields(model, prefer_related=(), max_fields=4):
    """
    Build a safe search_fields tuple for a model:
    - Always include 'pk'
    - Include model's own text fields (email/name/char/text)
    - For FK/OneToOne fields include related__<text_field> if the related model has a text field
    - Only include fields that actually exist
    """
    fields = ["pk"]
    meta = model._meta

    # prefer direct model fields first
    # find own text fields
    for f in meta.get_fields():
        if len(fields) >= max_fields:
            break
        if getattr(f, "concrete", False) and isinstance(f, (models.CharField, models.TextField, models.EmailField)):
            if f.name not in fields:
                fields.append(f.name)

    # then try prefer_related names (like 'user', 'medicine') -> add related__<textfield>
    for rel_name in prefer_related:
        if len(fields) >= max_fields:
            break
        try:
            f = meta.get_field(rel_name)
        except Exception:
            continue
        # only FK/OneToOne
        if isinstance(f, (models.ForeignKey, models.OneToOneField)):
            rel_model = f.remote_field.model
            txt = find_text_field_on_model(rel_model)
            if txt:
                candidate = f"{rel_name}__{txt}"
                if candidate not in fields:
                    fields.append(candidate)

    # final fallback: ensure limit and return tuple
    return tuple(fields[:max_fields])


# Mixin to allow numeric PK quick search (exact pk match)
class PKSearchMixin:
    def get_search_results(self, request, queryset, search_term):
        # numeric-only search -> exact pk match
        if search_term and search_term.isdigit():
            try:
                qs = queryset.filter(pk=int(search_term))
                return qs, False
            except Exception:
                pass
        # otherwise use default behavior
        return super().get_search_results(request, queryset, search_term)


# ---------- Medicine admin ----------
@admin.register(Medicine)
class MedicineAdmin(PKSearchMixin, admin.ModelAdmin):
    list_display = choose_fields_for_admin(Medicine, prefer=("name", "category", "price"))
    if len(list_display) > 1:
        list_display_links = (list_display[0], list_display[1])
    else:
        list_display_links = ("pk",)

    list_filter = tuple(
        f
        for f in ("category", "price", "is_active")
        if f in {f.name for f in Medicine._meta.get_fields()}
    )

    # safe search fields: model text fields + prefer related (none here)
    search_fields = build_safe_search_fields(Medicine, prefer_related=("category", ""))
    fields = tuple(f.name for f in Medicine._meta.fields if f.name != "id")
    ordering = ("-pk",)
    list_per_page = 20


# ---------- Cart admin ----------
@admin.register(Cart)
class CartAdmin(PKSearchMixin, admin.ModelAdmin):
    list_display = choose_fields_for_admin(Cart, prefer=("user", "medicine", "quantity"))
    if len(list_display) > 1:
        list_display_links = (list_display[0], list_display[1])
    else:
        list_display_links = ("pk",)

    list_filter = tuple(
        f for f in ("user", "medicine", "created_at") if f in {f.name for f in Cart._meta.get_fields()}
    )

    # Try to search by cart.pk, user email/name, medicine name
    search_fields = build_safe_search_fields(Cart, prefer_related=("user", "medicine"))

    list_per_page = 30

    def get_total_price(self, obj):
        try:
            return (
                getattr(obj, "total_price")()
                if callable(getattr(obj, "total_price", None))
                else getattr(obj, "total_price", "-")
            )
        except Exception:
            return "-"

    get_total_price.short_description = "Total Price"


# ---------- CheckoutDetails admin ----------
@admin.register(CheckoutDetails)
class CheckoutDetailsAdmin(PKSearchMixin, admin.ModelAdmin):
    list_display = choose_fields_for_admin(CheckoutDetails, prefer=("user", "prescription_file", "status"))
    if len(list_display) > 1:
        list_display_links = (list_display[0], list_display[1])
    else:
        list_display_links = ("pk",)

    # safe search fields: pk, user__email or user__name if available, order_id/invoice
    search_fields = build_safe_search_fields(CheckoutDetails, prefer_related=("user",))
    list_per_page = 25


# ---------- SignupUser admin ----------
@admin.register(SignupUser)
class SignupUserAdmin(admin.ModelAdmin):
    list_display = choose_fields_for_admin(SignupUser, prefer=("name", "email", "is_active"))
    if len(list_display) > 1:
        list_display_links = (list_display[0], list_display[1])
    else:
        list_display_links = ("pk",)

    # Build safe search for user: pk + name/email if present
    search_fields = build_safe_search_fields(SignupUser, prefer_related=())
    ordering = ("pk",)
    list_per_page = 25
