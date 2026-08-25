# 发布指南

[English](RELEASING.en.md)

项目使用 GitHub Actions 和 PyPI Trusted Publishing（OIDC）发布。构建任务无发布权限，
发布任务只接收已经测试和检查过的构建产物；仓库及 GitHub Secrets 均不需要保存 PyPI
API Token。

## 首次配置

这些设置只需由项目管理员完成一次。

1. 在 GitHub 仓库的 **Settings → Environments** 中创建名为 `pypi` 的 Environment。
2. 为 `pypi` 设置 Required reviewers，并将允许部署的 Git 标签限制为 `v*`。
3. 在 PyPI 项目 `chinese-address-generator` 的 **Manage → Publishing** 页面添加 GitHub
   Trusted Publisher：

   | 字段 | 值 |
   | --- | --- |
   | Owner | `Ginkgoty` |
   | Repository | `chinese-address-generator` |
   | Workflow name | `release.yml` |
   | Environment name | `pypi` |

PyPI 中的 workflow 文件名和 Environment 名称必须与
`.github/workflows/release.yml` 完全一致。

## 发布版本

1. 只修改 `chinese_address_generator/_version.py` 中的 `__version__`。构建系统会从该文件
   读取版本，避免维护两份版本号。
2. 将 `CHANGELOG.md` 中对应版本的 `Unreleased` 改为发布日期。
3. 在本机完整验证：

   ```bash
   uv lock --check
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest
   uv build
   uv run twine check dist/*
   ```

4. 审阅全部修改。获得维护者明确同意后，创建 GPG 签名 commit；未经同意不得提交。
5. 为相同版本创建并推送签名标签，例如：

   ```bash
   git tag -s v1.0.0 -m "Release 1.0.0"
   git push origin main
   git push origin v1.0.0
   ```

6. 在 GitHub 上从该标签创建 Release。只有 Release 的 **Publish release** 操作会触发
   发布 workflow；草稿不会上传 PyPI。
7. 检查 `build` 任务的测试和构建结果，然后由授权维护者批准 `pypi` Environment 部署。
8. 确认 PyPI 页面上的版本、wheel、源码包及数字证明均已出现。

workflow 会拒绝不以 `v` 开头的标签，也会拒绝标签版本与包版本不一致的 Release。

## 失败处理

PyPI 不允许覆盖同一版本的文件。如果失败发生在上传前，可以修复后重新运行；如果任一
构建产物已经上传，则必须发布一个新版本，不能删除后复用原版本号。不要在正常发布中
启用 `skip-existing`，否则可能掩盖不完整发布。
