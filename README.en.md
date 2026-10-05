# Beauty Live Handcards

A Chinese-first Agent Skill for beauty livestream product cards, image sets, ingredient explanations, and product bundles.

[中文](README.md) · [Downloads](https://github.com/ouyang-2019/beauty-live-handcards/releases/tag/v0.1.0) · [Installation](docs/installation.md) · [Five product galleries](examples/README.md)

## Install

WorkBuddy: import the WorkBuddy ZIP from the Release through Add Skill → Upload Skill.
Codex and other Agent Skills hosts: install the `skills/beauty-live-handcards` directory or the Agent Skills release archive.

## Input and output

Provide real packaging, ingredients/formula information, verified prices, and matching efficacy reports. Request a single card, a full image set, or a bundle card. The workflow combines product-specific scenes, ingredient explanations, promotional copy, and image review.

Image generation/editing and visual reading come from the host. The optional review-record gate requires Python 3.9+ and uses only the standard library.

## Status and examples

v0.1.0 is a public preview. The five galleries contain 37 existing product images from the author's project. The WorkBuddy file installation and package structure were checked; WorkBuddy image generation has not yet been verified.

## License

Skill rules, scripts, templates, and usage documentation are MIT licensed. Product showcase images, report excerpts inside images, and brand marks have separate [terms](examples/LICENSE.md).
