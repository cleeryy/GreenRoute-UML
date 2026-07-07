FROM nginx:alpine

# Cache-busting : reconstruit toujours avec les fichiers frais
ARG CACHE_BUST=1

# Suppression de la config par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/

# Contenu statique
COPY docs/ /usr/share/nginx/html/
COPY mockups/ /usr/share/nginx/html/mockups/
COPY diagrams/*.png /usr/share/nginx/html/diagrams/
COPY DAF_GreenRoute.md /usr/share/nginx/html/
COPY README.md /usr/share/nginx/html/

EXPOSE 4567

CMD ["nginx", "-g", "daemon off;"]
