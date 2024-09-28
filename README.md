# Projet_-_Phonetique_et_Synthese_de_la_Parole
Projet du cours de Phonétique et Synthèse de la Parole du M1 TAL (Traitement Automatique des Langues)


NGAUV Nicolas
M1 PluriTAL(INaLCO)





## Les 5 phrases :

Phrase 1 : "Le frêle chat noir dort sur le toit de la maison dans l'arbre."

Phrase 2 : "Les oiseaux chantent joyeusement dans le ciel bleu azur."

Phrase 3 : "La pluie fine tombe doucement sur la fenêtre froide."

Phrase 4 : "La vague de l'océan berce le navire endormi."

Phrase 5 : "Le vent siffle fort à travers les arbres de la forêt."





## Explications :


Dans le dossier de rendu se trouve :
- le dico (modifié pour mes phrases) sous format txt
- l'audio et le TextGrid des logatomes
- le présent README
- les synthèses des 5 phrases produites par le code
- le fichier contenant le code python (commenté) à exécuter pour produire les synthèses


Pour executer le code : python3 synthese_phrase.py
    -> la phrase synthétisée est enregistrée sous le nom "resultat.wav"





## Compléments :

Bien que d'une qualité acceptable, je pense, j'ai voulu essayé d'améliorer les synthèses obtenues de différentes manières :
- normaliser le volume
- réduire le bruit
- jouer encore plus en profondeur avec l'intonation, l'accentuation et la diction

J'ai cependant décidé de mettre ces fonctions en commentaire, voire de ne pas du tout les garder car avec des tests, je n'ai pas eu l'impression que la qualité générale des synthèses ait subi une amélioration importante.

Pour normaliser le volume avec librosa :
J'ai essayé et ça fonctionne, mais l'audio obtenu sonne moins clair que la version non-normalisé, comme un son plus étouffé, (surement dû à la compression et donc à la perte de qualité qui en résulte, vu la différence de taille avec la version non-normalisée).
J'ai donc décidé de tout mettre en commentaire pour ne pas l'utiliser (surtout que de base, la synthèse vocal obtenu sans cette normalisation a un volume plutôt équilibré je trouve), mais n'hésitez cependant pas à décommenter les instructions suivantes si vous souhaitez tester (en pensant également à décommenter les imports de bibliothèques utilisées ici : librosa et soundfile) !

    Peut_être besoin d'installer des packages pour tester :
    - pip install librosa
    - pip install soundfile

    -> la phrase synthétisée est enregistrée sous le nom "resultat_normalise.wav"

Pour réduire le bruit :
J'ai essayé avec la bibliothèque noisereduce, et ça fonctionne également, cependant je ne suis pas sûr que la qualité générale de la synthèse s'en trouve améliorée.
En effet, même s'il y a moins de bruit, à l'écoute on a l'impression d'entendre le son à travers un téléphone : sûrement car noisereduce a supprimé ou du moins altéré des parties du signal audio d'origine pour éliminer le bruit...
N'hésitez cependant pas à décommenter les instructions suivantes si vous souhaitez tester (en pensant également à décommenter les imports de bibliothèques utilisées ici : noisereduce et wavfile) !

    Peut_être besoin d'installer des packages pour tester :
    - pip install noisereduce
    - pip install torch torchvision torchaudio

    -> la phrase synthétisée est enregistrée sous le nom "resultat_reduced_noise.wav"

J'ai aussi essayé de voir comment jouer encore plus en profondeur avec l'intonation, l'accentuation et la diction afin d'avoir des synthèses de phrases avec une prosodie plus proche de l'humain (en tout cas, de moi).
Cependant, dans la majorité des cas il fallait que j'utilise des bibliothèques ou des outils de synthèse vocale avancés qui offrent des contrôles plus spécifiques sur l'intonation et d'autres caractéristiques vocales.
Je pouvais également modifier avec Parselmouth la f0, la durée ou l'intensité de certaines parties des phrases, de certains segments, mais au détriment de la qualité de la voix, et de sa naturalité ; ou alors sans obtenir d'améliorations significatifs (d'après les résultats que j'ai obtenu lors de mes tests)... Ce qui serait contre-productif : je ne les ai donc pas implémentés dans la version finale du rendu
(Rendu qui permet déjà d'obtenir, je pense, des résultats acceptables au niveau des phrases obtenu via la synthèse de la parole)...
