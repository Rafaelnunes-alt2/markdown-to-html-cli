# markdown-to-html-cli

Conversor de Markdown para HTML por linha de comando, Python puro sem
dependência externa. Suporte a títulos, negrito, itálico, código inline,
bloco de código, listas e parágrafos. Saída HTML5 mínimo com CSS embutido.

## Uso

    python3 md2html.py --in doc.md --out doc.html
    cat doc.md | python3 md2html.py > doc.html

## Segurança

Input escapado antes de aplicar transformações, arquivo até 16 MB, nenhum
`eval`, nenhum import fora da stdlib. Exit 2 em falha de leitura/escrita,
2 em arquivo muito grande.

## Testes validados

    título h1, negrito strong, itálico em, código inline code — OK
    lista ul/li — OK
    fence ``` vira pre/code com escape — OK
    stdin sem --in funciona — OK
    --out CSV grava arquivo — OK

## Limitações

Subconjunto didático: sem tabelas, imagem, link, task list nem nota
de rodapé. Não é CommonMark completo. Útil para documentos simples
e CI de README.

## Próximos passos

Modo watch, suporte a links e imagens, flag --no-style.

## Autor

Rafael Nunes — [@Rafaelnunes-alt2](https://github.com/Rafaelnunes-alt2)
