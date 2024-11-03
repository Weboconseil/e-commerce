import streamlit as st
import pandas as pd

def calculate_financials(inputs):
    # Calcul du nombre de commandes
    nb_commandes = inputs['trafic_mensuel'] * (inputs['taux_conversion'] / 100)
    
    # Calcul du chiffre d'affaires pour chaque panier
    ca_panier1 = nb_commandes * inputs['prix_achat_1'] * (1 + inputs['marge_1'] / 100)
    ca_panier2 = nb_commandes * inputs['prix_achat_2'] * (1 + inputs['marge_2'] / 100)
    
    ca_total = ca_panier1 + ca_panier2
    
    # Calcul des charges variables
    commissions = (ca_total * 0.029) + (nb_commandes * 0.30)
    frais_livraison = nb_commandes * inputs['frais_livraison']
    charges_variables = commissions + frais_livraison
    
    # Calcul des charges fixes mensuelles
    charges_fixes = (
        inputs['abonnement_shopify'] +
        inputs['consultant_seo'] +
        (inputs['nom_domaine'] / 12) +  # Conversion annuel en mensuel
        inputs['marketing']
    )
    
    # Calculs finaux
    marge_brute = ca_total - charges_variables
    resultat_avant_impot = marge_brute - charges_fixes
    impot = resultat_avant_impot * 0.25 if resultat_avant_impot > 0 else 0
    resultat_net = resultat_avant_impot - impot
    
    return {
        'Nombre de commandes': round(nb_commandes, 2),
        'Chiffre d\'affaires Panier 1': round(ca_panier1, 2),
        'Chiffre d\'affaires Panier 2': round(ca_panier2, 2),
        'Chiffre d\'affaires Total': round(ca_total, 2),
        'Charges Variables': round(charges_variables, 2),
        'Charges Fixes': round(charges_fixes, 2),
        'Marge Brute': round(marge_brute, 2),
        'Résultat avant impôt': round(resultat_avant_impot, 2),
        'Impôt': round(impot, 2),
        'Résultat Net': round(resultat_net, 2)
    }

def main():
    st.title('Calculateur de Rentabilité E-commerce')
    
    st.header('1. Coûts des paniers')
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Panier 1')
        prix_achat_1 = st.number_input('Prix d\'achat', key='prix1', value=10.0)
        frais_annexes_1 = st.number_input('Frais annexes', key='frais1', value=2.0)
    
    with col2:
        st.subheader('Panier 2')
        prix_achat_2 = st.number_input('Prix d\'achat', key='prix2', value=15.0)
        frais_annexes_2 = st.number_input('Frais annexes', key='frais2', value=3.0)
    
    st.header('2. Marges bénéficiaires')
    col3, col4 = st.columns(2)
    
    with col3:
        marge_1 = st.slider('Marge Panier 1 (%)', 0, 200, 60)
    
    with col4:
        marge_2 = st.slider('Marge Panier 2 (%)', 0, 200, 60)
    
    st.header('3. Trafic et Conversion')
    trafic_mensuel = st.number_input('Trafic mensuel', value=1000)
    taux_conversion = st.slider('Taux de conversion (%)', 0.0, 10.0, 2.0, 0.1)
    
    st.header('4. Charges d\'exploitation')
    
    st.subheader('Charges variables')
    frais_livraison = st.number_input('Frais de livraison par commande', value=6.0)
    
    st.subheader('Charges fixes')
    col5, col6 = st.columns(2)
    
    with col5:
        abonnement_shopify = st.number_input('Abonnement Shopify mensuel', value=32.0)
        consultant_seo = st.number_input('Consultant SEO mensuel', value=200.0)
    
    with col6:
        nom_domaine = st.number_input('Nom de domaine annuel', value=15.0)
        marketing = st.number_input('Budget Marketing mensuel', value=250.0)
    
    # Rassembler toutes les entrées
    inputs = {
        'prix_achat_1': prix_achat_1,
        'prix_achat_2': prix_achat_2,
        'marge_1': marge_1,
        'marge_2': marge_2,
        'trafic_mensuel': trafic_mensuel,
        'taux_conversion': taux_conversion,
        'frais_livraison': frais_livraison,
        'abonnement_shopify': abonnement_shopify,
        'consultant_seo': consultant_seo,
        'nom_domaine': nom_domaine,
        'marketing': marketing
    }
    
    # Calculer et afficher les résultats
    if st.button('Calculer les prévisions'):
        resultats = calculate_financials(inputs)
        
        st.header('Résultats des Prévisions Financières')
        
        # Créer un DataFrame pour un affichage plus propre
        df_resultats = pd.DataFrame(list(resultats.items()), columns=['Métrique', 'Valeur'])
        df_resultats['Valeur'] = df_resultats['Valeur'].apply(lambda x: f"{x:,.2f} €")
        
        st.table(df_resultats)
        
        # Afficher quelques KPIs importants dans des métriques séparées
        col7, col8, col9 = st.columns(3)
        with col7:
            st.metric("Chiffre d'affaires mensuel", f"{resultats['Chiffre d\'affaires Total']:,.2f} €")
        with col8:
            st.metric("Marge Brute", f"{resultats['Marge Brute']:,.2f} €")
        with col9:
            st.metric("Résultat Net", f"{resultats['Résultat Net']:,.2f} €")

if __name__ == '__main__':
    main()
