#### Nome

WSPR decoy

#### PT-BR

Nos anos que antecederam a Guerra, radioamadores construíram transmissores do tipo *beacon* extremamente sólidos e duráveis. Esses transmissores podem ser ouvidos até hoje nas ondas de rádio que chegam a Rhiza, e estão documentados até mesmo nos livros didáticos do ensino médio!

Estudando os arquivos contidos na cápsula do tempo colocada na ilha pela Telefonica e outras empresas na década de 2020, Laura deparou-se recentemente com uma implementação um tanto curiosa de um transmissor WSPR.

Esse transmissor insere uma segunda modulação por cima do WSPR, quase imperceptível ao olho nu. O indicativo de chamada do autor do código corresponde justamente a uma das estações *beacon* que podem ser ouvidas até hoje. Essa estação está na área onde um dia esteve localizada a Universidade Federal de São Carlos.

Será que esses transmissores podem revelar algo que não é contado pela história oficial do governo? Talvez eles estejam ligados a algum movimento de resistência das pessoas do continente!

Infelizmente, a cápsula do tempo contém apenas o código fonte do codificador. Você consegue implementar o decodificador correspondente? Obtenha as gravações das transmissões de rádio que são emitidas a cada 10 min e forneça-as ao seu decodificador, recuperando o conteúdo do arquivo `flag.txt` do transmissor.

**Nota importante aos competidores de 2021**

Aproveite que o planeta ainda não foi devastado! Existem muitos receptores KiwiSDR, OpenWebRX e WebSDR públicos na internet. Utilize esses receptores para gravar o áudio da transmissão. Você também pode consultar o [histórico da WSPRNet](https://wsprnet.org/olddb?mode=html&band=all&limit=10000&findcall=PU2UID&findreporter=&sort=date) para verificar quais regiões do planeta estão recebendo o sinal em um dado momento, ou programar-se sabendo quais regiões costumam recebê-lo em determinado horário.

Recomendamos que você faça, o mais cedo possível, **pelo menos** 4 gravações do sinal com boa relação sinal ruído (SNR) e com pouco *fading*. Comece a gravar as transmissões mesmo antes de implementar o seu decodificador.

**Autores**: [thotypous](https://github.com/thotypous), [racerxdl](https://github.com/racerxdl)

**Agradecimentos especiais**: [marcoslaerte](https://github.com/marcoslaerte), [nutc4k3](https://github.com/nutc4k3)


#### EN

In the years leading up to the war, radio amateurs built extraordinarily reliable and durable beacon transmitters. These transmitters can still be heard today on the radio waves that reach Rhiza and are even documented in high school textbooks!

Studying the files contained in the time capsule placed on the island by Telefonica and other companies in the 2020s, Laura recently came across a somewhat curious implementation of a WSPR transmitter.

This transmitter inserts a secondary modulation over WSPR, almost imperceptible to the naked eye. The call sign of the code's author corresponds precisely to one of the beacon stations that can be heard till today. This station is in the area where the Federal University of São Carlos was once located.

Can these transmitters reveal something that is not told in official government accounts? Perhaps they are linked to some resistance movement by the people overseas!

Unfortunately, the time capsule contains only the encoder's source code. Can you implement the corresponding decoder? Record the beacons transmitted every 10 min and feed them to your decoder, retrieving the contents of the transmitter's `flag.txt` file.

**Important note to 2021 competitors**

Use to your advantage that the planet has not yet been devastated! There are many public KiwiSDR, OpenWebRX and WebSDR receivers on the internet. Use these receivers to record the audio from the transmitter. You can also consult the WSPRNet history to observe which regions of the planet are receiving the signal at any given time. Schedule future recordings based on the knowledge of which areas usually receive the beacons at a particular time of the day. We recommend that you record, as soon as possible, **at least** 4 broadcasts of the signal with a good signal-to-noise ratio (SNR) and without significant fading. Start recording the broadcasts even before implementing your decoder.

**Authors**: [thotypous](https://github.com/thotypous), [racerxdl](https://github.com/racerxdl)

**Special thanks to**: [marcoslaerte](https://github.com/marcoslaerte), [nutc4k3](https://github.com/nutc4k3)


#### Flag

`CTF-BR{COME!-MY_QTH_FOR_SHE!TER}`


#### Hints

1. Fornecer link do [OpenWebRX localizado na UFSCar](https://pu2uid.duckdns.org).

2. Fornecer as [duas gravações de alta qualidade do PY1EME](https://drive.google.com/drive/folders/1kHCD5thhziNtsk_4n21TSKwCTKrimB5E?usp=sharing), que são suficientes para decodificador o sinal.

