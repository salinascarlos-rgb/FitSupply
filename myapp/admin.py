from django.contrib import admin
from .models import LogAuditoria

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'modelo', 'objeto_id', 'descripcion')
    list_filter = ('modelo', 'accion', 'fecha')
    search_fields = ('usuario__username', 'modelo', 'descripcion')

