import numpy as np
from scipy.stats import shapiro
import pandas as pd 

class DataCleaner:
    def __init__(self, input_file, output_file):
       
        
        self.input_file = input_file
        self.output_file = output_file
        # Charger les données depuis le fichier CSV
        self.df = pd.read_csv(self.input_file)

        # Appliquer le nettoyage des données
        self.replace_missing_values()

        # Sauvegarder les données nettoyées dans un fichier CSV
        self.save_cleaned_data()

        # Afficher les résultats du nettoyage
        self.show_missing_values()

    def replace_missing_values(self):
       
        for column in self.df.columns:
            # Ignorer les colonnes non numériques
            if self.df[column].dtype != 'object':
                # Extraire la colonne sans valeurs manquantes
                column_data = self.df[column].dropna()

                # Effectuer le test de Shapiro-Wilk pour la normalité
                shapiro_test = shapiro(column_data)

                # Remplacer les valeurs manquantes en fonction de la normalité
                if shapiro_test.pvalue > 0.05:  # Si la distribution est normale
                    self.df[column] = self.df[column].fillna(self.df[column].mean())
                else:  # Si la distribution n'est pas normale
                    self.df[column] = self.df[column].fillna(self.df[column].median())

    def save_cleaned_data(self):
        """
        Sauvegarde le DataFrame nettoyé dans un fichier CSV.
        """
        self.df.to_csv(self.output_file, index=False)
        print(f"🔹 Les données nettoyées ont été sauvegardées dans : {self.output_file}")

    def show_missing_values(self):
        """
        Affiche le nombre de valeurs manquantes restantes après nettoyage.
        """
        print("🔹 Résultats après nettoyage des données :\n")
        print(self.df.isnull().sum())  # Afficher le nombre de valeurs manquantes restantes


# Exemple d'utilisation : 
input_file = "data/TemperatureRainFall.csv"  # Chemin vers votre fichier CSV d'entrée
output_file = "data/Cleaned_TemperatureRainFall.csv"  # Chemin du fichier de sortie

# Créer une instance de la classe DataCleaner
cleaner = DataCleaner(input_file, output_file)
