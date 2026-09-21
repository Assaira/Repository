import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 1. CONFIGURATION DE LA PAGE
# =========================================================

st.set_page_config(
    page_title="Analyse Financière Personnelle",
    page_icon="💰",
    layout="wide"
)

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuration de la page
st.set_page_config(
    page_title="Analyse Financière Personnelle",
    page_icon="💰",
    layout="wide"
)

# ... (ton code CSS personnalisé qu'on a mis juste avant) ...

# =========================================================
# BARRE LATÉRALE DE NAVIGATION PROFESSIONNELLE
# =========================================================
with st.sidebar:
    selected = option_menu(
        menu_title="Mon Application",
        options=["Tableau de bord", "Transactions", "Analyses", "Alertes & Paramètres"],
        icons=["house-door-fill", "wallet2", "graph-up-arrow", "gear-fill"],  # Icônes modernes
        menu_icon="cash-stack",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F9FBF9"},
            "icon": {"color": "#2E7D32", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px",
                "border-radius": "8px",
                "--hover-color": "#E8F5E9",
            },
            "nav-link-selected": {
                "background-color": "#2E7D32", 
                "color": "white",
                "font-weight": "500"
            },
        }
    )

# =========================================================
# GESTION DES PAGES SELON LA SÉLECTION DU MENU
# =========================================================

if selected == "Tableau de bord":
    st.title("📊 Tableau de bord financier")
    st.write("Bienvenue sur ton espace de suivi global.")
    # Mets ici le code de ton tableau de bord (métriques, graphiques principaux...)

elif selected == "Transactions":
    st.title("💳 Historique des transactions")
    st.write("Consulte et filtre l'ensemble de tes opérations.")
    # Mets ici ton tableau de transactions / filtres

elif selected == "Analyses":
    st.title("📈 Analyses et Prévisions")
    st.write("Visualise tes tendances de dépenses.")
    # Mets ici tes graphiques d'analyse avancés

elif selected == "Alertes & Paramètres":
    st.title("⚙️ Seuils et Paramètres")
    st.write("Gère tes alertes de budget.")
    # Mets ici ton système d'alertes

# =========================================================
# 2. CATÉGORISATION AUTOMATIQUE
# =========================================================

regles_categories = {

    "Alimentation": [
        "supermarché",
        "supermarche",
        "marché",
        "marche",
        "restaurant",
        "boulangerie",
        "épicerie",
        "epicerie",
        "alimentation"
    ],

    "Transport": [
        "taxi",
        "transport",
        "carburant",
        "essence",
        "station",
        "bus"
    ],

    "Logement": [
        "loyer",
        "maison",
        "électricité",
        "electricite",
        "eau"
    ],

    "Télécommunication": [
        "orange",
        "moov",
        "telecom",
        "internet",
        "wifi",
        "téléphone",
        "telephone",
        "forfait",
        "crédit"
    ],

    "Santé": [
        "pharmacie",
        "clinique",
        "hôpital",
        "hopital",
        "médecin",
        "medecin",
        "consultation"
    ],

    "Shopping": [
        "vêtement",
        "vetement",
        "chaussure",
        "boutique",
        "shopping",
        "habillement"
    ],

    "Loisirs": [
        "cinéma",
        "cinema",
        "sortie",
        "loisir",
        "jeu"
    ],

    "Abonnements": [
        "netflix",
        "spotify",
        "abonnement",
        "application",
        "subscription"
    ],

    "Éducation": [
        "formation",
        "livre",
        "fourniture",
        "école",
        "ecole",
        "université",
        "universite"
    ]
}


def categoriser_transaction(libelle):

    libelle = str(libelle).lower()

    for categorie, mots_cles in regles_categories.items():

        for mot in mots_cles:

            if mot in libelle:
                return categorie

    return "Autres"


# =========================================================
# 3. TITRE DE L'APPLICATION
# =========================================================

st.title("💰 Analyse Financière Personnelle")

st.markdown(
    "### Tableau de bord de suivi et d'analyse des finances personnelles"
)


# =========================================================
# 4. CHARGEMENT DU FICHIER (EXCEL / CSV)
# =========================================================

st.sidebar.header("📁 Importation des données")

fichier_importe = st.sidebar.file_uploader(
    "Importer un fichier (Excel ou CSV)", type=["xlsx", "xls", "csv"]
)

if fichier_importe is not None:
  try:
    if fichier_importe.name.endswith(".csv"):
      df = pd.read_csv(fichier_importe)
    else:
      df = pd.read_excel(fichier_importe)
    st.sidebar.success("Fichier importé avec succès !")
  except Exception as e:
    st.sidebar.error(f"Erreur lors de la lecture du fichier : {e}")
    # Fichier de secours par défaut en cas d'erreur
    fichier = "transactions_fictives_analyse_financiere.xlsx"
    df = pd.read_excel(fichier)
else:
  # Fichier par défaut si aucun fichier n'est glissé-déposé
  fichier = "transactions_fictives_analyse_financiere.xlsx"
  df = pd.read_excel(fichier)


# =========================================================
# 5. CONVERSION DE LA DATE
# =========================================================

df["date"] = pd.to_datetime(df["date"])


# =========================================================
# 6. APPLICATION DE LA CATÉGORISATION AUTOMATIQUE
# =========================================================

df["categorie_automatique"] = df["libelle"].apply(
    categoriser_transaction
)


# =========================================================
# 7. FILTRES
# =========================================================

st.sidebar.header("🔎 Filtres")

date_min = df["date"].min().date()
date_max = df["date"].max().date()

date_selection = st.sidebar.date_input(
    "Période",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

categories = ["Toutes"] + sorted(
    df["categorie_automatique"].dropna().unique().tolist()
)

categorie_selection = st.sidebar.selectbox(
    "Catégorie",
    categories
)


# =========================================================
# 8. FILTRAGE DES DONNÉES
# =========================================================

df_filtre = df.copy()

if len(date_selection) == 2:

    date_debut = pd.Timestamp(date_selection[0])
    date_fin = pd.Timestamp(date_selection[1])

    df_filtre = df_filtre[
        (df_filtre["date"] >= date_debut)
        &
        (df_filtre["date"] <= date_fin)
    ]

if categorie_selection != "Toutes":

    df_filtre = df_filtre[
        df_filtre["categorie_automatique"]
        == categorie_selection
    ]
    
# =========================================================
# CONFIGURATION DES ALERTES (DANS LA BARRE LATÉRALE)
# =========================================================
st.sidebar.header("🚨 Paramètres d'alertes")
seuil_alerte_global = st.sidebar.number_input(
    "Seuil d'alerte budget global (FCFA)",
    min_value=10000,
    value=150000,
    step=10000
)


# =========================================================
# 9. INDICATEURS
# =========================================================

revenus = df_filtre.loc[
    df_filtre["type"] == "Revenu",
    "montant"
].sum()

depenses = df_filtre.loc[
    df_filtre["type"] == "Dépense",
    "montant"
].sum()

solde = revenus - depenses

nombre_transactions = len(df_filtre)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Revenus",
        f"{revenus:,.0f} FCFA"
    )


with col2:

    st.metric(
        "💸 Dépenses",
        f"{depenses:,.0f} FCFA"
    )


with col3:

    st.metric(
        "💵 Solde",
        f"{solde:,.0f} FCFA"
    )


with col4:

    st.metric(
        "🧾 Transactions",
        nombre_transactions
    )


# =========================================================
# 10. RÉSULTAT DE LA CATÉGORISATION
# =========================================================

st.subheader("🏷️ Catégorisation automatique")

st.dataframe(
    df_filtre[
        [
            "date",
            "libelle",
            "montant",
            "type",
            "categorie_automatique"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 10.1 ÉVALUATION DE LA CATÉGORISATION
# =========================================================

st.subheader("🎯 Évaluation de la catégorisation")

# Comparaison entre la catégorie réelle et la catégorie automatique
df_filtre["correct"] = (
    df_filtre["categorie"]
    == df_filtre["categorie_automatique"]
)

nombre_correct = df_filtre["correct"].sum()
nombre_total = len(df_filtre)

if nombre_total > 0:

    taux_reussite = (
        nombre_correct / nombre_total
    ) * 100

else:

    taux_reussite = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Transactions correctement classées",
        nombre_correct
    )

with col2:
    st.metric(
        "Transactions incorrectes",
        nombre_total - nombre_correct
    )

with col3:
    st.metric(
        "Taux de réussite",
        f"{taux_reussite:.1f}%"
    )


# Tableau de comparaison
st.write("### Comparaison")

st.dataframe(
    df_filtre[
        [
            "libelle",
            "categorie",
            "categorie_automatique",
            "correct"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 14. DÉTECTION DES DÉPENSES INHABITUELLES
# =========================================================

st.subheader("🚨 Détection des dépenses inhabituelles")

# On isole uniquement les dépenses du dataframe filtré
depenses_df = df_filtre[df_filtre["type"] == "Dépense"].copy()

if not depenses_df.empty:
  # Calcul de la moyenne et de l'écart-type par catégorie
  moyenne = depenses_df.groupby("categorie_automatique")["montant"].transform(
      "mean"
  )
  ecart_type = depenses_df.groupby("categorie_automatique")[
      "montant"
  ].transform("std")

  # Remplacement des valeurs NaN par 0 si l'écart-type ne peut pas être calculé (ex: 1 seule transaction dans la catégorie)
  ecart_type = ecart_type.fillna(0)

  # Définition du seuil d'anomalie : moyenne + (2 * écart-type)
  depenses_df["seuil"] = moyenne + (2 * ecart_type)

  # Filtrage des transactions qui dépassent le seuil
  anomalies = depenses_df[depenses_df["montant"] > depenses_df["seuil"]]

  if not anomalies.empty:
    st.warning(
        "⚠️ Les transactions suivantes dépassent vos habitudes de dépenses pour"
        " ces catégories :"
    )
    st.dataframe(
        anomalies[
            [
                "date",
                "libelle",
                "montant",
                "categorie_automatique",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.success(
        "✅ Aucune dépense inhabituelle détectée pour cette sélection."
    )
else:
  st.info("Pas assez de données de dépenses pour analyser les anomalies.")
  
# =========================================================
# 15. PRÉVISION DU BUDGET POUR LE MOIS SUIVANT
# =========================================================

st.subheader("🔮 Prévision des dépenses du mois suivant")

# On extrait uniquement les dépenses
df_depenses = df[df["type"] == "Dépense"].copy()

if not df_depenses.empty:
    # S'assurer que la colonne mois existe
    if "mois" not in df_depenses.columns:
        df_depenses["mois"] = df_depenses["date"].dt.to_period("M").astype(str)
        
    # Calcul des dépenses totales par mois
    depenses_mensuelles_totales = df_depenses.groupby("mois")["montant"].sum()
    
    # Calcul de la moyenne mensuelle des dépenses globales
    prevision_globale = depenses_mensuelles_totales.mean()
    
    col_prev1, col_prev2 = st.columns(2)
    
    with col_prev1:
        st.metric(
            "Estimation globale du mois prochain",
            f"{prevision_globale:,.0f} FCFA"
        )
        
    with col_prev2:
        st.info(
            "💡 Cette prévision est calculée en faisant la moyenne "
            "des dépenses totales des mois précédents enregistrés dans l'historique."
        )
else:
    st.info("Pas assez de données pour effectuer des prévisions budgétaires.")


# =========================================================
# 11. GRAPHIQUE : DÉPENSES PAR CATÉGORIE
# =========================================================

st.subheader("📊Répartition des dépenses par catégorie")

depenses_categories = df_filtre[
    df_filtre["type"] == "Dépense"
].groupby(
    "categorie_automatique"
)["montant"].sum().reset_index()


fig_categories = px.pie(
    depenses_categories,
    names="categorie_automatique",
    values="montant",
    hole=0.4
)

st.plotly_chart(
    fig_categories,
    use_container_width=True
)


# =========================================================
# 12. GRAPHIQUE : ÉVOLUTION MENSUELLE
# =========================================================

st.subheader("📈 Évolution mensuelle des dépenses")

df_filtre["mois"] = (
    df_filtre["date"]
    .dt.to_period("M")
    .astype(str)
)


depenses_mensuelles = df_filtre[
    df_filtre["type"] == "Dépense"
].groupby(
    "mois"
)["montant"].sum().reset_index()


fig_mensuel = px.bar(
    depenses_mensuelles,
    x="mois",
    y="montant",
    labels={
        "mois": "Mois",
        "montant": "Dépenses (FCFA)"
    }
)

st.plotly_chart(
    fig_mensuel,
    use_container_width=True
)


# =========================================================
# 13. TRANSACTIONS
# =========================================================

st.subheader("📋 Transactions")

st.dataframe(
    df_filtre,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 13.5. PRÉVISION DU BUDGET PAR CATÉGORIE
# =========================================================

st.subheader("📊 Prévisions détaillées par catégorie pour le mois prochain")

df_depenses_cat = df[df["type"] == "Dépense"].copy()

if not df_depenses_cat.empty:
    # S'assurer que la colonne mois existe
    if "mois" not in df_depenses_cat.columns:
        df_depenses_cat["mois"] = df_depenses_cat["date"].dt.to_period("M").astype(str)
        
    # Calculer le total des dépenses par mois et par catégorie
    suivi_mensuel_cat = df_depenses_cat.groupby(["mois", "categorie_automatique"])["montant"].sum().reset_index()
    
    # Calculer la moyenne mensuelle par catégorie
    prevision_par_cat = suivi_mensuel_cat.groupby("categorie_automatique")["montant"].mean().reset_index()
    prevision_par_cat.columns = ["Catégorie", "Dépense estimée (FCFA)"]
    
    # Arrondir les montants pour plus de lisibilité
    prevision_par_cat["Dépense estimée (FCFA)"] = prevision_par_cat["Dépense estimée (FCFA)"].round(0)
    
    # Affichage sous forme de tableau interactif
    st.dataframe(
        prevision_par_cat,
        use_container_width=True,
        hide_index=True
    )
    
    # Optionnel : Graphique en barres des prévisions par catégorie
    fig_prev_cat = px.bar(
        prevision_par_cat,
        x="Catégorie",
        y="Dépense estimée (FCFA)",
        title="Estimation des dépenses par poste pour le mois prochain",
        text_auto=".2s"
    )
    st.plotly_chart(fig_prev_cat, use_container_width=True)
else:
    st.info("Pas assez de données pour établir des prévisions par catégorie.")
    
# =========================================================
# 13.6. SYSTÈME D'ALERTES DYNAMIQUES
# =========================================================

st.subheader("🚨 Système d'alertes et de dépassements")

# Calcul des dépenses totales de la sélection actuelle
total_depenses_selection = df_filtre.loc[df_filtre["type"] == "Dépense", "montant"].sum()

# Vérification de l'alerte globale
if total_depenses_selection > seuil_alerte_global:
    st.error(
        f"🚨 **ALERTE ROUGE :** Vos dépenses actuelles ({total_depenses_selection:,.0f} FCFA) "
        f"ont dépassé le seuil d'alerte défini de {seuil_alerte_global:,.0f} FCFA !"
    )
elif total_depenses_selection >= (seuil_alerte_global * 0.8):
    st.warning(
        f"⚠️ **Attention :** Vous avez atteint plus de 80% de votre seuil d'alerte "
        f"({total_depenses_selection:,.0f} FCFA / {seuil_alerte_global:,.0f} FCFA)."
    )
else:
    st.success(
        f"✅ **Statut budgétaire sain :** Vos dépenses ({total_depenses_selection:,.0f} FCFA) "
        f"sont en dessous du seuil d'alerte."
    )

# Vérification par catégorie (alerte si une catégorie représente plus de 40% des dépenses)
if not depenses_categories.empty:
    depenses_categories["part"] = (depenses_categories["montant"] / depenses_categories["montant"].sum()) * 100
    categories_Lourdes = depenses_categories[depenses_categories["part"] > 40]
    
    if not categories_Lourdes.empty:
        for index, row in categories_Lourdes.iterrows():
            st.info(
                f"💡 **Note d'attention :** La catégorie **{row['categorie_automatique']}** "
                f"représente à elle seule {row['part']:.1f}% de vos dépenses totales."
            )    

# =========================================================
# 16. CONSEILS FINANCIERS AUTOMATIQUES
# =========================================================

st.subheader("💡 Conseils financiers et recommandations")

# Analyse conditionnelle pour générer des conseils adaptés
if solde < 0:
    st.error(
        "⚠️ **Alerte budgétaire :** Vos dépenses dépassent vos revenus sur cette période. "
        "Il est recommandé de revoir vos catégories de dépenses non essentielles (Loisirs, Shopping) pour rééquilibrer votre budget."
    )
elif taux_reussite < 80:
    st.info(
        "💡 **Conseil d'optimisation :** Le taux de réussite de la catégorisation automatique est inférieur à 80%. "
        "Pensez à enrichir le dictionnaire des `regles_categories` au début de votre code pour affiner le classement de vos libellés."
    )
else:
    st.success(
        "✨ **Excellente gestion :** Vos finances se portent bien sur cette période, vos revenus couvrent vos dépenses "
        "et la catégorisation fonctionne de manière optimale. Continuez ainsi !"
    )
