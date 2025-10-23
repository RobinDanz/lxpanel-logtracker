#include <gtk/gtk.h>
#include <libappindicator/app-indicator.h>
#include <glib.h>

// Variables globales pour l’icône et menu
AppIndicator *indicator;
GtkWidget *menu;

// Fonction appelée pour quitter l’application
static void quit_app(GtkMenuItem *item, gpointer data) {
    gtk_main_quit();
}

// Fonction pour créer le menu
static GtkWidget* create_menu() {
    GtkWidget *menu = gtk_menu_new();
    GtkWidget *quit_item = gtk_menu_item_new_with_label("Quitter");
    g_signal_connect(quit_item, "activate", G_CALLBACK(quit_app), NULL);
    gtk_menu_shell_append(GTK_MENU_SHELL(menu), quit_item);
    gtk_widget_show_all(menu);
    return menu;
}

// Fonction pour changer l’icône (animation)
static gboolean toggle_icon(gpointer data) {
    static gboolean state = FALSE;
    if(state) {
        app_indicator_set_icon(indicator, "dialog-information"); // icône idle
    } else {
        app_indicator_set_icon(indicator, "dialog-warning"); // icône active
    }
    state = !state;
    return TRUE; // pour continuer le timer
}

int main(int argc, char **argv) {
    gtk_init(&argc, &argv);

    // Crée l’indicateur AppIndicator
    indicator = app_indicator_new(
        "logmon",                   // id
        "dialog-information",       // icône initiale (nom d’icône GTK)
        APP_INDICATOR_CATEGORY_APPLICATION_STATUS
    );

    app_indicator_set_status(indicator, APP_INDICATOR_STATUS_ACTIVE);

    // Crée le menu
    menu = create_menu();
    app_indicator_set_menu(indicator, GTK_MENU(menu));

    // Timer pour changer l’icône toutes les 500ms (animation)
    g_timeout_add(500, toggle_icon, NULL);

    gtk_main();
    return 0;
}