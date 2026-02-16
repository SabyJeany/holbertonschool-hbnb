
┌─────────────┐
│ JEANY       │  "Je veux m'inscrire avec saby@example.com"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SERVEUR   │  "Attends, je vérifie si cet email existe déjà..."
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  BASE DE    │  "Je cherche saby@example.com..."
│  DONNÉES    │  "Trouvé ! Marie utilise déjà cet email !"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SERVEUR   │  "Désolé Jeany, cet email est déjà pris !"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    JEANY    │  Reçoit : ❌ "Erreur 400 : Email déjà utilisé"
└─────────────┘
