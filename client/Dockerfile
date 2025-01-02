# Utiliser une image Node.js officielle
FROM node:14

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code de l'application
COPY . .

# Construire l'application pour la production
RUN npm run build

# Installer 'serve' pour servir l'application
RUN npm install -g serve

# Exposer le port utilisé par l'application
EXPOSE 3000

# Commande pour démarrer l'application
CMD ["serve", "-s", "build", "-l", "3000"]
