<h1 align="center">Projectile Motion (Lançamento Oblíquo)</h1>
<p style align="center">
  <a href="#formulas">Formulas</a> -
  <a href="#bibliotecas">Bibliotecas</a> -
  <a href="#executar">Executar</a> 
</p>

# Formulas
Para o caso do lançamento oblíquo, a velocidade considerada na vertical será a componente Vy, sendo assim, podemos escrever:

![image](https://user-images.githubusercontent.com/55333375/177892623-3e751c58-e362-4852-9a2b-28d8a4bbb135.png)

O tempo destacado acima refere-se à subida do objeto, logo, o tempo total do movimento será o dobro.

![image](https://user-images.githubusercontent.com/55333375/177892676-c2924646-2e03-41aa-96c7-39b623652868.png)

A equação final para a determinação do alcance horizontal em um lançamento oblíquo é:

![image](https://user-images.githubusercontent.com/55333375/177892703-148a6407-c65b-48e7-bc95-fe360eec00c9.png)

O alcance será o máximo possível quando o ângulo de lançamento for igual a 45°. Como o ângulo é multiplicado por dois na equação do alcance, o seno calculado será o de 90°, que corresponde ao máximo valor de seno possível, assim o alcance será o máximo possível.

A imagem abaixo indica as possíveis trajetórias para lançamentos oblíquos executados sobre ângulos diversos. Observe que o maior alcance ocorre quando o ângulo de lançamento é igual a 45º.

![image](https://user-images.githubusercontent.com/55333375/177892719-1ecb5ef7-52ad-4c18-bfee-6bef4d26875d.png)

A equação abaixo determina a altura máxima atingida por um objeto que executa movimento oblíquo.

![image](https://user-images.githubusercontent.com/55333375/177892731-e3c5c0ae-7075-4af5-9c1d-003e615bdafb.png)


# Bibliotecas 
+ Foi utilizado a biblioteca **tkinter** para a criação de toda a interface gráfica.
+ Foi utilizado a bibliteca **numpy** para a resolução dos cálculos.
+ Foi utilizado a biblioteca **matplotlib** para plotar o grafico e gerar a animação.
# Executar
|   Comando   |    Função  |    
| -----------------------|-----------------------|
|    *sudo apt install python3-pip*     |     instala o pip para facilitar na hora de instalar as bibliotecas  |   
|     *pip install tk*     |   instala a biblioteca tkinter    |      
|     *pip install numpy*     |    instala a biblioteca numpy    |      
|*pip install matplotlib* | instala a biblioteca matplotlib
| *python3 main.py*| executa o programa
