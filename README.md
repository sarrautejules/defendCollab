# Idée du projet
Simple API avec gestion des datasets et des media uploads.
=> Aider les lives de @anisayari pour que la communauté puisse aider à construire les datasets.
- [x] Principaux Modèles et Controllers
- [x] Mise en place des templates
- [ ] Gestion de la sécurité (user, droits pour la configuration des datasets)
    - [x] Mise en place du JWT
    - [x] Mise en place des permissions
    - [ ] Mise en place modération du contenu
    - [ ] Mise en place modération des utilisateurs
- [ ] Nettoyage du code
- [ ] Révision de la méthode de mise en production

# Contribuer
Vous pouvez ouvrir des PR

Utilisation de docker et docker compose
démarrer en mode détaché
```
docker-compose up -d --build
```
démarrer avec les logs attachés au terminal
```
docker-compose up --build
```

### Bootstrap Flask API
Based on https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
