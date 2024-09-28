import parselmouth
import textgrids
import matplotlib.pyplot as plt
#import librosa
#import soundfile as sf
#import noisereduce as nr
#from scipy.io import wavfile





# NGAUV Nicolas 
# M1 PluriTAL(INaLCO)





def main():
    ouverture()
    creation_dico()

    # Liste avec toutes les phrases que l'on va proposer à l'utilisateur
    liste_phrases = ["le frêle chat noir dort sur le toit de la maison dans l'arbre",
                    "les oiseaux chantent joyeusement dans le ciel bleu azur",
                    "la pluie fine tombe doucement sur la fenêtre froide",
                    "la vague de l'océan berce le navire endormi",
                    "le vent siffle fort à travers les arbres de la forêt"]

    # Demande à l'utilisateur quelle phrase il voudrait synthétiser
    p = ''
    while (p != '1') and (p != '2') and (p != '3') and (p != '4') and (p != '5'):
        for l in liste_phrases:
            print(l, end="\n")
        p = input("Donnez le numéro de la phrase que vous souhaitez synthétiser (1, 2, 3, 4 ou 5) : ")
    # Affecte la phrase choisie par l'utilisateur à la variable avec laquelle on va travailler
    phrase = liste_phrases[int(p) - 1]

    transcription(phrase)
    synthese_phrase()





def ouverture():
    global son
    global grille
    global synthese
    # Chemins vers les fichiers nécessaires
    son = 'Logatomes_NGAUV-Nicolas.wav'
    grille = 'Logatomes_NGAUV-Nicolas.TextGrid'
    synthese = 'resultat.wav'

    global sound
    global segmentation
    # Chargement du fichier sonore et du TextGrid pour la segmentation
    sound = parselmouth.Sound(son)
    segmentation = textgrids.TextGrid(grille)

    # Pour la visualisation 
    #plt.figure()
    #plt.plot(sound.xs(),sound.values.T)
    #plt.xlabel("temps (s)")
    #plt.ylabel("amplitude")
    #plt.show()





# Initialisation et remplissage du dictionnaire de prononciation SAMPA
def creation_dico():
    global dico
    dico = {}
    with open('dico_UTF8.txt', 'r') as dic:
        for line in dic:
            ortho, sampa = line.strip().split('\t')
            dico[ortho] = sampa





# Transcription de la phrase orthographique vers la phrase phonetique 
# en prenant en compte les apostrophes (pour les phrases 1 et 4)
def transcription(phrase):
    phrase = phrase.replace("'","' ")
    global phrase_phonetique
    phrase_phonetique = []

    # Conversion de chaque mot de la phrase en phonétique selon le dictionnaire SAMPA
    for mot in phrase.split(" "):
        phrase_phonetique.append(dico[mot])
    phrase_phonetique = "".join(phrase_phonetique)
    phrase_phonetique = "_" + phrase_phonetique + "_"

    # On affiche la phrase en SAMPA dans le terminal
    print(phrase_phonetique)





# Fonction pour extraire un diphone à partir des phonèmes
def extraction_diphone(diphones, diphone1, diphone2, sound):
    for i in range(len(diphones) - 1):
        if diphones[i].text == diphone1 and diphones[i+1].text == diphone2:
            # Calcul des milieux des phonèmes pour extraire le diphone
            milieu_phoneme1 = (diphones[i].xmin + diphones[i].xmax) / 2
            milieu_phoneme2 = (diphones[i+1].xmin + diphones[i+1].xmax) / 2

            # Recherche des points de croisement zéro les plus proches
            milieu_phoneme1 = sound.get_nearest_zero_crossing(milieu_phoneme1, 1)
            milieu_phoneme2 = sound.get_nearest_zero_crossing(milieu_phoneme2, 1)

            # Extraction du diphone
            return sound.extract_part(milieu_phoneme1, milieu_phoneme2, parselmouth.WindowShape.RECTANGULAR, 1, False)
    return None





def synthese_phrase():
    # Concaténation des diphones pour former la phrase
    sound_concat = None
    for l in range(len(phrase_phonetique) - 1):
        diphone1 = phrase_phonetique[l]
        diphone2 = phrase_phonetique[l + 1]
        extrait = extraction_diphone(segmentation['phonemes'], diphone1, diphone2, sound)
        if extrait:
            # Si aucun son n'a encore été concaténé, initialiser sound_concat
            if sound_concat is None:
                sound_concat = extrait
            # Sinon, concaténer le nouveau diphone avec les précédents
            else:
                sound_concat = parselmouth.Sound.concatenate([sound_concat, extrait], overlap=0.005)

    # Sauvegarde du résultat final si sound_concat n'est pas vide dans un fichier audio "resultat.wav"
    if sound_concat:
        sound_concat.save(synthese, 'WAV')



    #COMPLÉMENTS 
    # Pour normaliser le volume avec librosa : j'ai essayé et ça fonctionne,
    # mais l'audio obtenu sonne moins clair que la version non-normalisé, comme un son plus étouffé, 
    # (surement dû à la compression et donc à la perte de qualité qui en résulte, vu la différence de taille avec la version non-normalisée)
    # donc j'ai décidé de tout mettre en commentaire pour ne pas l'utiliser (surtout que de base, la synthèse vocal obtenu sans cette normalisation a un volume plutôt équilibré je trouve)
    # n'hésitez cependant pas à décommenter les instructions suivantes si vous souhaitez tester (en pensant également à décommenter les imports de bibliothèques utilisées ici) !
        
    # Charge le fichier audio
    #audio, sr = librosa.load('resultat.wav')

    # Appliquer la normalisation du volume
    #resultat_normalise = librosa.util.normalize(audio)

    # Chemin pour enregistrer l'audio normalisé
    #chemin_fichier_normalise = 'resultat_normalise.wav'

    # Enregistrer l'audio normalisé dans un fichier WAV
    #sf.write(chemin_fichier_normalise, resultat_normalise, sr)



    # Pour réduire le bruit, j'ai essayé avec la bibliothèque noisereduce, et ça fonctionne également
    # Cependant, je ne suis pas sûr que la qualité générale de la synthèse s'en trouve améliorée
    # En effet, même s'il y a moins de bruit, à l'écoute on a l'impression d'entendre le son à travers un téléphone
    # Sûrement car noisereduce a supprimé ou du moins altéré des parties du signal audio d'origine pour éliminer le bruit...
    # n'hésitez cependant pas à décommenter les instructions suivantes si vous souhaitez tester (en pensant également à décommenter les imports de bibliothèques utilisées ici) !

    # Chargement du fichier audio
    #rate, data = wavfile.read("resultat.wav")
        
    # Réduction du bruit
    #reduced_noise = nr.reduce_noise(y=data, sr=rate)
    #wavfile.write("resultat_reduced_noise.wav", rate, reduced_noise)





# J'ai aussi essayé de voir comment jouer encore plus en profondeur avec l'intonation, l'accentuation et la diction
# afin d'avoir des synthèses de phrases avec une prosodie plus proche de l'humain (en tout cas, de moi) 
# mais aussi de réduire le bruit dans les résultats des synthèses vocales obtenues
# cependant, dans la majorité des cas il fallait que j'utilise des bibliothèques ou des outils de synthèse vocale avancés 
# qui offrent des contrôles plus spécifiques sur l'intonation et d'autres caractéristiques vocales,
# ou alors je pouvais aussi modifier avec parselmouth la f0, la durée ou l'intensité de certaines parties des phrases, de certains segments,
# mais au détriment de la qualité de la voix, et de sa naturalité ; ou alors sans obtenir d'améliorations significatifs (d'après les résultats que j'ai obtenu lors de mes tests)
# ce qui serait contre-productif : je ne les ai donc pas implémentés dans la version finale du rendu 
# (rendu qui permet d'obtenir, je pense, quand même des résultats acceptables au niveau des phrases obtenu via la synthèse vocale)...
    




if __name__ == "__main__":
    main()